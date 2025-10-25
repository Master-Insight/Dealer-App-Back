# app/modules/users/logic/services.py
from app.libraries.exceptions.app_exceptions import (
    AuthError,
    NotFoundError,
    ValidationError,
)
from ..data.dao import UserDAO
from app.services.supabase_client import supabase


class UserService:
    def __init__(self):
        self.dao = UserDAO()

    def register_user(self, email: str, password: str, role: str = "user"):

        try:
            """Crea usuario en Supabase Auth."""
            auth_user = supabase.auth.sign_up({"email": email, "password": password})

            """ Crear perfil en tu tabla user_profiles """
            profile = {
                "id": auth_user.user.id,
                "email": email,
                "role": role,
            }
            return self.dao.create_profile(profile)

        except Exception as e:
            if "User already registered" in str(e):
                raise ValidationError("El email ya está registrado")
            if "Password should be at least 6 characters" in str(e):

                raise ValidationError("La contraseña debe tener al menos 6 caracteres")

            raise AuthError("Error al registrar usuario", details={"error": str(e)})

    def list_users(self):
        return self.dao.get_all()

    def get_user(self, user_id: str):
        user = supabase.table("users").select("*").eq("id", user_id).execute()
        if not user.data:
            raise NotFoundError(f"Usuario con id {user_id} no encontrado")
        return user.data[0]
