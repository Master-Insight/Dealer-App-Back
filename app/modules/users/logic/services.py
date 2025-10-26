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

        # 1) Intentar crear usuario en Auth (o confirmar existencia)
        try:
            """Crea usuario en Supabase Auth."""
            auth_user = supabase.auth.sign_up({"email": email, "password": password})
            user_id = auth_user.user.id

        except Exception as e:
            error_str = str(e)

            # Caso: Contraseña inválida
            if "Password should be at least 6 characters" in error_str:
                raise ValidationError("La contraseña debe tener al menos 6 caracteres")

            # Caso: Email ya registrado -> Sign-in para obtener ID real
            if "User already registered" in error_str:
                # El usuario ya existe en Auth; opcionalmente confirmamos credenciales
                auth_user = supabase.auth.sign_in_with_password(
                    {"email": email, "password": password}
                )
                if not auth_user or not auth_user.user:
                    raise AuthError(
                        "Email duplicado. No se puede loguear. Credenciales inválidas o usuario bloqueado",
                        details={"supabase_error": error_str},
                    )
                user_id = auth_user.user.id

            else:
                raise AuthError(
                    "Error al registrar usuario", details={"supabase_error": error_str}
                )

        # 2) Revisar/asegurar el perfil (el trigger debería haberlo creado)
        profile = self.dao.get_by_email(email)
        if profile:
            # 2a) Si el perfil existe, asegurar el role (idempotente)
            current_role = profile.get("role")
            if current_role != role:
                # Si querés restringir quién puede cambiar roles, validalo antes
                updated = self.dao.update_role_by_email(email, role)
                # `update_role_by_email` debería devolver el registro actualizado
                return updated
            # No hay cambios de rol → devolver perfil existente
            return profile

        # 3) Si NO existe perfil (trigger falló), lo creamos manualmente
        #    (si no tenemos user_id, este es un buen lugar para resolverlo si es crítico)
        new_profile = {
            "id": user_id,  # si es None y tu tabla lo requiere NOT NULL, resolvé antes el id
            "email": email,
            "role": role,
        }
        created = self.dao.create_profile(new_profile)
        return created

    def login(self, email: str, password: str):
        try:
            auth_user = supabase.auth.sign_in_with_password(
                {"email": email, "password": password}
            )

            if not auth_user.user:
                raise AuthError("Credenciales inválidas")

            profile = self.dao.get_by_email(email)
            return {
                "token": auth_user.session.access_token,
                "profile": profile,
            }

        except Exception:
            raise AuthError("Credenciales inválidas")

    def list_users(self):
        return self.dao.get_all()

    def get_user(self, user_id: str):
        user = self.dao.get_by_id(user_id)
        return user

    def delete_user(self, user_id: str):
        try:
            # 1️⃣ Verificar si el usuario existe en tu tabla
            user = self.dao.get_by_id(user_id)
            if not user:
                raise NotFoundError(f"Usuario con id {user_id} no encontrado")

            # 2️⃣ Eliminar perfil en tu base de datos
            self.dao.delete_profile(user_id)

            # 3️⃣ Eliminar usuario en Supabase Auth (requiere Service Role Key)
            supabase.auth.admin.delete_user(user_id)

            return {"message": f"Usuario {user_id} eliminado correctamente"}

        except NotFoundError:
            raise
        except Exception as e:
            raise AuthError("Error al eliminar usuario", details={"error": str(e)})
