from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models.user import User
from app.api.v1.schemas.user import UserCreate, UserRead
from app.services.user_service import UserService
from app.api.v1.dependencies.auth import validate_roles

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserRead)
def create_user(
    payload: UserCreate,
    db: Session = Depends(get_db),
    _=Depends(validate_roles(["admin"])),
):
    existing = db.query(User).filter(User.username == payload.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    user = UserService.create_user(
        db=db, username=payload.username, password=payload.password, role=payload.role
    )

    return user


@router.get("/", response_model=List[UserRead])
def list_users(
    db: Session = Depends(get_db),
    _: User = Depends(validate_roles(["admin", "manager"])),
):
    return UserService.get_all_users(db)
