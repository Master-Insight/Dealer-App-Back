# app/libraries/auth/dependencies.py
from fastapi import Header
from app.libraries.exceptions.app_exceptions import AuthError
from app.services.supabase_client import supabase


async def get_current_user(authorization: str = Header(...)):

    # Validar header presente
    if not authorization:
        raise AuthError("Falta token de autorización")

    # Validar formato
    if not authorization.startswith("Bearer "):
        raise AuthError("Token inválido")

    # Validar token no vacío
    token = authorization.replace("Bearer ", "").strip()
    if not token:
        raise AuthError("Token inválido o vacío")

    # Validar token via Supabase
    try:
        user = supabase.auth.get_user(token)
        if not user or not user.user:
            raise AuthError("Token inválido o expirado")
        return user.user

    except Exception as e:
        raise AuthError("Token inválido", details={"supabase_error": str(e)})
