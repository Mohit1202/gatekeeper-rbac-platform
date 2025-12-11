import datetime
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.models.user import User
from app.db.session import get_db
from app.core.security import (
    create_access_token,
    authenticate_user,
    create_password_hash,
)

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": str(user.id), "role": user.role})

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/init")
def init_admin(db: Session = Depends(get_db)):
    user_count = db.query(User).count()
    if user_count > 0:
        raise HTTPException(status_code=403, detail="Already initialized")

    admin = User(
        username="admin",
        password_hash=create_password_hash("admin123"),
        role="admin",
        created_at=datetime.datetime.utcnow(),
    )
    db.add(admin)
    db.commit()

    return {"message": "Admin created"}
