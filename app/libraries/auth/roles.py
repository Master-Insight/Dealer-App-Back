# app/libraries/auth/roles.py
from fastapi import Depends
from app.libraries.exceptions.app_exceptions import AuthError
from .dependencies import get_current_user
from app.modules.users.logic.services import UserService


def require_role(allowed_roles: list[str]):
    async def role_checker(current_user=Depends(get_current_user)):
        user_service = UserService()
        profile = user_service.get_user_by_email(current_user.email)
        if not profile or profile["role"] not in allowed_roles:
            raise AuthError("No tienes permiso")
        return profile

    return role_checker
