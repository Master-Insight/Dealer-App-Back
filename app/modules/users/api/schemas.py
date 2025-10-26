# app/modules/users/api/schemas.py
from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr


class RoleEnum(str, Enum):
    root = "root"
    admin = "admin"
    user = "user"


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: str
    role: Optional[RoleEnum] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class LoginResponse(BaseModel):
    token: str
    profile: Optional[User] = None


class LogoutResponse(BaseModel):
    status: str


class UserSummary(BaseModel):
    id: str
    email: EmailStr


class DeleteUserResponse(BaseModel):
    user: Optional[UserSummary] = None
