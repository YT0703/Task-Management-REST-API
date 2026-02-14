# app/crud/task.py

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


class CRUDTask(CRUDBase[Task, TaskCreate, TaskUpdate]):
    def get_tasks_by_owner(
        self, db: Session, owner_id: int, skip: int = 0, limit: int = 100
    ) -> list[Task]:
        return (
            db.query(Task)
            .filter(Task.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create_with_owner(
        self, db: Session, obj_in: TaskCreate, owner_id: int
    ) -> Task:
        db_obj = Task(**obj_in.model_dump(), owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


task = CRUDTask(Task)



