# app/modules/users/api/routes.py
from typing import List

from fastapi import APIRouter, Depends, Header

from app.libraries.auth.dependencies import get_current_user
from app.libraries.utils.response_models import ApiResponse
from .controller import UserController
from .schemas import (
    DeleteUserResponse,
    LoginResponse,
    LogoutResponse,
    User,
    UserCreate,
    UserLogin,
)

router = APIRouter()
controller = UserController()


@router.post("/register", response_model=ApiResponse[User])
def register_user(user: UserCreate):
    return controller.register_user(user)


@router.post("/login", response_model=ApiResponse[LoginResponse])
def login(user: UserLogin):
    return controller.login(user)


@router.post("/logout", response_model=ApiResponse[LogoutResponse])
def logout():
    return controller.logout()


@router.get("/me", response_model=ApiResponse[User])
def get_me(current_user=Depends(get_current_user)):
    return controller.get_me(current_user)


@router.get("/", response_model=ApiResponse[List[User]])
def list_users():
    return controller.list_users()


@router.delete("/delete/{user_id}", response_model=ApiResponse[DeleteUserResponse])
def delete_user(user_id: str):
    return controller.delete_user(user_id)
