# app/libraries/auth/dependencies.py
from fastapi import Header
from app.libraries.exceptions.app_exceptions import AuthError
from app.services.supabase_client import supabase


async def get_current_user(authorization: str = Header(...)):

    if not authorization.startswith("Bearer "):
        raise AuthError("Token inválido")

    token = authorization.replace("Bearer ", "")

    """Verifica token JWT de Supabase."""
    try:
        user = supabase.auth.get_user(token)
        if not user or not user.user:
            raise AuthError("Token inválido o expirado")
        return user.user

    except Exception as e:
        raise AuthError("Token inválido", details={"supabase_error": e})
