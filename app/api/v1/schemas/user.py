from pydantic import BaseModel
from datetime import datetime

from app.constants import Role


class UserBase(BaseModel):
    username: str
    role: Role


class UserCreate(UserBase):
    password: str
    model_config = {
        "json_schema_extra": {
            "examples": [
                {"username": "john", "role": "viewer", "password": "password123"}
            ]
        }
    }


class UserRead(UserBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}
