# app/modules/users/logic/services.py
from ..data.dao import UserDAO
from app.libraries.customs.base_service import BaseService

class UserService:
    def __init__(self):
        self.dao = UserDAO()

    # def register_user(self, email: str, password: str, role: str = "user"):
    #     """Crea usuario en Supabase Auth y su perfil."""
    #     auth_user = supabase.auth.sign_up({"email": email, "password": password})
    #     if not auth_user.user:
    #         raise ValueError("Error creando usuario en Supabase")

    #     profile = {
    #         "id": auth_user.user.id,
    #         "email": email,
    #         "role": role,
    #     }
    #     return self.dao.create_profile(profile)

    def list_users(self):
        return self.dao.get_all()

    def get_user_by_email(self, email: str):
        return self.dao.get_by_email(email)