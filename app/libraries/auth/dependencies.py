# app/libraries/auth/dependencies.py
from fastapi import Depends, HTTPException, Header
from app.services.supabase_client import supabase

async def get_current_user(authorization: str = Header(...)):
    """Verifica token JWT de Supabase."""
    token = authorization.replace("Bearer ", "")
    try:
        user = supabase.auth.get_user(token)
        if not user or not user.user:
            raise HTTPException(status_code=401, detail="Token inválido o expirado")
        return user.user
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
