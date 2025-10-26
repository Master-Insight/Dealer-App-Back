# app/modules/users/api/routes.py
from fastapi import APIRouter
from .schemas import UserCreate, ResponseModel
from .controller import UserController

router = APIRouter()
controller = UserController()


@router.get("/", response_model=ResponseModel)
def list_users():
    return controller.list_users()


@router.post("/register", response_model=ResponseModel)
def register_user(user: UserCreate):
    return controller.register_user(user)


@router.delete("/delete/{user_id}", response_model=ResponseModel)
def delete_user(user_id: str):
    return controller.delete_user(user_id)
