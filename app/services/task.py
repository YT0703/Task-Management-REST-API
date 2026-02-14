# app/services/task.py

from sqlalchemy.orm import Session

from app.crud.task import task as crud_task
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


def create_task(db: Session, task_in: TaskCreate, owner_id: int) -> Task:
    return crud_task.create_with_owner(db, obj_in=task_in, owner_id=owner_id)


def get_task(db: Session, task_id: int) -> Task | None:
    return crud_task.get(db, id=task_id)


def get_user_tasks(
    db: Session, owner_id: int, skip: int = 0, limit: int = 100
) -> list[Task]:
    return crud_task.get_tasks_by_owner(db, owner_id=owner_id, skip=skip, limit=limit)


def update_task(db: Session, db_task: Task, task_in: TaskUpdate) -> Task:
    return crud_task.update(db, db_obj=db_task, obj_in=task_in)


def delete_task(db: Session, task_id: int) -> Task | None:
    return crud_task.remove(db, id=task_id)



