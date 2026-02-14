# app/services/user.py

from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.crud.user import user as crud_user
from app.models.user import User
from app.schemas.user import UserCreate


def create_user(db: Session, user_in: UserCreate) -> User:
    hashed_password = get_password_hash(user_in.password)
    user_in.password = hashed_password  # Update the Pydantic model with hashed password
    return crud_user.create(db, obj_in=user_in)


def get_user_by_email(db: Session, email: str) -> User | None:
    return crud_user.get_by_email(db, email=email)


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return crud_user.get(db, id=user_id)



