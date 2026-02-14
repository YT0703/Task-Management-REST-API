# app/schemas/task.py

from pydantic import BaseModel


class TaskBase(BaseModel):
    title: str
    description: str | None = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    completed: bool | None = None


class TaskInDBBase(TaskBase):
    id: int
    completed: bool = False
    owner_id: int

    model_config = {"from_attributes": True}


class Task(TaskInDBBase):
    pass



