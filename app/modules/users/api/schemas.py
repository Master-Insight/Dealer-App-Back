# app/modules/users/api/schemas.py
from typing import List, Optional, Union
from pydantic import BaseModel
from datetime import datetime

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    role: str = "user"


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: str = "user"


class User(UserBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True


class ResponseModel(BaseModel):
    success: bool
    message: str
    data: Optional[Union[User, List[User], dict, str]] = None
