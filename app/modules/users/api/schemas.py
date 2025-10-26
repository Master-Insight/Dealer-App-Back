# app/modules/users/api/schemas.py
from enum import Enum
from typing import List, Optional, Union
from pydantic import BaseModel, EmailStr
from datetime import datetime


class RoleEnum(str, Enum):
    code = "code"
    admin = "admin"
    user = "user"


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserBase(BaseModel):
    email: EmailStr
    role: Optional[RoleEnum] = RoleEnum.user


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True


class ResponseModel(BaseModel):
    success: bool
    message: str
    data: Optional[Union[User, List[User], dict, str]] = None
