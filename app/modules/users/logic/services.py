# app/modules/users/logic/services.py
from fastapi import HTTPException
from app.libraries.utils.response_builder import ResponseBuilder
from ..data.dao import UserDAO
from app.services.supabase_client import supabase


class UserService:
    def __init__(self):
        self.dao = UserDAO()

    def register_user(self, email: str, password: str, role: str = "user"):
        try:
            """Crea usuario en Supabase Auth."""
            auth_user = supabase.auth.sign_up({"email": email, "password": password})
            if not auth_user.user:
                raise ValueError("Error creando usuario en Supabase")

            """ Crear perfil en tu tabla user_profiles """
            profile = {
                "id": auth_user.user.id,
                "email": email,
                "role": role,
            }
            return self.dao.create_profile(profile)

        except ValueError as ve:
            ResponseBuilder.error("Datos inválidos", str(ve), 400)
        except Exception as e:
            ResponseBuilder.error("Error interno al registrar usuario", str(e), 500)

    def list_users(self):
        return self.dao.get_all()

    def get_user_by_email(self, email: str):
        return self.dao.get_by_email(email)
