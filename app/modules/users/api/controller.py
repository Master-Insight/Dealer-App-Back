# app/modules/s/api/controller.py
from app.libraries.utils.response_builder import ResponseBuilder
from .schemas import UserCreate
from ..logic.services import UserService


class UserController:
    def __init__(self):
        self.service = UserService()

    def list_users(self):
        """Obtiene todos los registros."""
        users = self.service.list_users()
        return ResponseBuilder.success(
            data=users, message="Usuarios obtenidos correctamente"
        )

    def login(self, login_data):
        data = self.service.login(login_data.email, login_data.password)
        return ResponseBuilder.success(data, "Login exitoso ✅")

    def logout(self):
        result = self.service.logout()
        return ResponseBuilder.success(result, "Sesión cerrada ✅")

    def get_me(self, current_user):
        data = self.service.get_user(current_user.id)
        return ResponseBuilder.success(data, "Perfil del usuario obtenido")

    # TODO en caso de usar un role distinto  a "user" deberia confirmar medidas de seguridad para limitar acción
    def register_user(self, user: UserCreate):
        profile = self.service.register_user(
            user.email, user.password
        )  # se quita x seguridad -->, user.role
        return ResponseBuilder.success(profile, "Usuario registrado correctamente")

    def delete_user(self, id: str):
        result = self.service.delete_user(id)
        return ResponseBuilder.success(result, "Usuario eliminado correctamente")
