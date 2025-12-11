import datetime

from sqlalchemy.orm import Session
from app.db.models.user import User
from app.core.security import create_password_hash
from app.core.logging_config import logger


class UserService:
    @staticmethod
    def create_user(db: Session, username: str, password: str, role: str):
        logger.info("Creating new user with username: %s", username)
        hashed_pw = create_password_hash(password)

        user = User(
            username=username,
            password_hash=hashed_pw,
            role=role,
            created_at=datetime.datetime.utcnow(),
        )

        db.add(user)
        db.commit()
        db.refresh(user)
        logger.info("User created successfully")
        return user

    @staticmethod
    def get_all_users(db: Session):
        logger.info("Retrieving all users")
        return db.query(User).all()
