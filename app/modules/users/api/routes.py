# app/modules/users/api/routes.py
from fastapi import APIRouter, Depends, HTTPException
from .schemas import User, UserCreate
from .controller import UserController

router = APIRouter()
controller = UserController()

# @router.post("/register", response_model=User)
# def register_user(user: UserCreate):
#     return controller.register_user(user)

@router.get("/", response_model=list[User])
def list_users():
    return controller.list_users()
