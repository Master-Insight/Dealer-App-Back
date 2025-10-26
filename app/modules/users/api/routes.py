# app/modules/users/api/routes.py
from fastapi import APIRouter, Depends, Header
from app.libraries.auth.dependencies import get_current_user
from .schemas import UserCreate, ResponseModel, UserLogin
from .controller import UserController

router = APIRouter()
controller = UserController()


@router.post("/register", response_model=ResponseModel)
def register_user(user: UserCreate):
    return controller.register_user(user)


@router.post("/login", response_model=ResponseModel)
def login(user: UserLogin):
    return controller.login(user)


@router.post("/logout", response_model=ResponseModel)
def logout():
    return controller.logout()


@router.get("/me", response_model=ResponseModel)
def get_me(current_user=Depends(get_current_user)):
    return controller.get_me(current_user)


@router.get("/", response_model=ResponseModel)
def list_users():
    return controller.list_users()


@router.delete("/delete/{user_id}", response_model=ResponseModel)
def delete_user(user_id: str):
    return controller.delete_user(user_id)
