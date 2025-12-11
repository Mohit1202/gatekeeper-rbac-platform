from fastapi import Depends
from typing import Annotated, List
from fastapi import HTTPException

from app.core.security import get_current_active_user
from app.db.models.user import User


def validate_roles(required_roles: List[str]):
    def validator(user: Annotated[User, Depends(get_current_active_user)]):
        if user.role not in required_roles:
            raise HTTPException(
                status_code=403,
                detail=f"Access Not Granted, user role not valid for: {user.username}",
            )
        return user

    return validator
