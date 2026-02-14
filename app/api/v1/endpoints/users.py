# app/api/v1/endpoints/users.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.handler import get_current_active_user
from app.db.session import get_db
from app.models.user import User as DBUser
from app.schemas.user import User, UserCreate
from app.services.user import create_user, get_user_by_email

router = APIRouter()


@router.post("/users/", response_model=User, status_code=status.HTTP_201_CREATED)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)) -> DBUser:
    user = get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this username already exists in the system.",
        )
    user = create_user(db, user_in=user_in)
    return user


@router.get("/users/me/", response_model=User)
def read_users_me(current_user: DBUser = Depends(get_current_active_user)) -> DBUser:
    return current_user



