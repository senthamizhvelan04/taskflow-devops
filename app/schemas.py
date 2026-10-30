from datetime import datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

Priority = Literal["low", "medium", "high"]
Status = Literal["todo", "in_progress", "done"]

class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    description: str = Field(default="", max_length=2000)
    priority: Priority = "medium"

class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=120)
    description: str | None = Field(default=None, max_length=2000)
    priority: Priority | None = None
    status: Status | None = None

class TaskRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    description: str
    priority: Priority
    status: Status
    created_at: datetime
