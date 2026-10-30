import time
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException, Response
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from . import models, schemas

BASE_DIR = Path(__file__).resolve().parent

REQUEST_COUNT = Counter(
    "taskflow_http_requests_total",
    "Total HTTP requests handled by TaskFlow",
    ["method", "endpoint", "status_code"],
)
REQUEST_LATENCY = Histogram(
    "taskflow_http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint"],
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Convenient for a learning project. For production, use Alembic migrations.
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="TaskFlow API",
    description="A DevOps portfolio task-management API with PostgreSQL and Prometheus metrics.",
    version="1.0.0",
    lifespan=lifespan,
)

@app.middleware("http")
async def collect_metrics(request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start
    route = request.url.path
    REQUEST_COUNT.labels(request.method, route, str(response.status_code)).inc()
    REQUEST_LATENCY.labels(request.method, route).observe(duration)
    return response

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

@app.get("/", include_in_schema=False)
def home():
    return FileResponse(BASE_DIR / "static" / "index.html")

@app.get("/health", tags=["operations"])
def health():
    return {"status": "healthy", "service": "taskflow-api"}

@app.get("/ready", tags=["operations"])
def readiness(db: Session = Depends(get_db)):
    try:
        db.execute(__import__("sqlalchemy").text("SELECT 1"))
        return {"status": "ready", "database": "connected"}
    except Exception as exc:
        raise HTTPException(status_code=503, detail="Database is not ready") from exc

@app.get("/metrics", include_in_schema=False)
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/api/tasks", response_model=list[schemas.TaskRead], tags=["tasks"])
def list_tasks(status: str | None = None, db: Session = Depends(get_db)):
    query = db.query(models.Task)
    if status:
        if status not in {"todo", "in_progress", "done"}:
            raise HTTPException(status_code=400, detail="Invalid status filter")
        query = query.filter(models.Task.status == status)
    return query.order_by(models.Task.id.desc()).all()

@app.post("/api/tasks", response_model=schemas.TaskRead, status_code=201, tags=["tasks"])
def create_task(payload: schemas.TaskCreate, db: Session = Depends(get_db)):
    task = models.Task(**payload.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@app.patch("/api/tasks/{task_id}", response_model=schemas.TaskRead, tags=["tasks"])
def update_task(task_id: int, payload: schemas.TaskUpdate, db: Session = Depends(get_db)):
    task = db.get(models.Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task

@app.delete("/api/tasks/{task_id}", status_code=204, tags=["tasks"])
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.get(models.Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return Response(status_code=204)
