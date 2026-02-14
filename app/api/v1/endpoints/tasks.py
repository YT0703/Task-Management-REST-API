# app/api/v1/endpoints/tasks.py

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.handler import get_current_active_user
from app.db.session import get_db
from app.models.user import User as DBUser
from app.schemas.task import Task, TaskCreate, TaskUpdate
from app.services.task import create_task, delete_task, get_task, get_user_tasks, update_task

router = APIRouter()


@router.post("/tasks/", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_user_task(
    task_in: TaskCreate,
    current_user: DBUser = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> Any:
    task = create_task(db, task_in=task_in, owner_id=current_user.id)
    return task


@router.get("/tasks/", response_model=list[Task])
def read_user_tasks(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: DBUser = Depends(get_current_active_user),
) -> Any:
    tasks = get_user_tasks(db, owner_id=current_user.id, skip=skip, limit=limit)
    return tasks


@router.get("/tasks/{task_id}", response_model=Task)
def read_task_by_id(
    task_id: int,
    current_user: DBUser = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> Any:
    task = get_task(db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this task")
    return task


@router.put("/tasks/{task_id}", response_model=Task)
def update_user_task(
    task_id: int,
    task_in: TaskUpdate,
    current_user: DBUser = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> Any:
    db_task = get_task(db, task_id=task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    if db_task.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this task")
    task = update_task(db, db_task=db_task, task_in=task_in)
    return task


@router.delete("/tasks/{task_id}", response_model=Task)
def delete_user_task(
    task_id: int,
    current_user: DBUser = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> Any:
    db_task = get_task(db, task_id=task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    if db_task.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this task")
    task = delete_task(db, task_id=task_id)
    return task



