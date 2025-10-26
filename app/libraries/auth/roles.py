# app/libraries/auth/roles.py
from fastapi import Depends
from app.libraries.exceptions.app_exceptions import AuthError
from .dependencies import get_current_user
from app.modules.users.logic.services import UserService


def require_role(allowed_roles: list[str]):
    async def role_checker(current_user=Depends(get_current_user)):
        user_service = UserService()

        profile = user_service.get_user_by_email(current_user.email)

        if not profile:
            raise AuthError("Perfil no encontrado para este usuario")

        role = (
            profile.get("role")
            if isinstance(profile, dict)
            else getattr(profile, "role", None)
        )

        # print("\nPerfil encontrado:", profile)
        # print("Rol del usuario:", role)
        # print("Roles permitidos:", allowed_roles)

        if role not in allowed_roles:
            raise AuthError("No tienes permiso para acceder a este recurso")

        return profile

    return role_checker
