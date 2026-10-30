import os
from pathlib import Path

# Use a separate SQLite database for automated tests.
test_db = Path("test_taskflow.db")
if test_db.exists():
    test_db.unlink()
os.environ["DATABASE_URL"] = f"sqlite:///{test_db.resolve()}"

from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine

Base.metadata.create_all(bind=engine)
client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_task_lifecycle():
    created = client.post("/api/tasks", json={
        "title": "Write Jenkins pipeline",
        "description": "Build and test the app",
        "priority": "high"
    })
    assert created.status_code == 201
    task = created.json()
    task_id = task["id"]
    assert task["status"] == "todo"

    updated = client.patch(f"/api/tasks/{task_id}", json={"status": "in_progress"})
    assert updated.status_code == 200
    assert updated.json()["status"] == "in_progress"

    listed = client.get("/api/tasks")
    assert listed.status_code == 200
    assert any(item["id"] == task_id for item in listed.json())

    deleted = client.delete(f"/api/tasks/{task_id}")
    assert deleted.status_code == 204

    missing = client.get("/api/tasks")
    assert all(item["id"] != task_id for item in missing.json())

def test_invalid_priority():
    response = client.post("/api/tasks", json={"title": "Bad task", "priority": "urgent"})
    assert response.status_code == 422
