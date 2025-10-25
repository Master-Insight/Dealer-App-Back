# app/modules/s/api/controller.py
from app.libraries.customs.controller_base import CustomController
from app.libraries.utils.response_builder import ResponseBuilder
from .schemas import User, UserCreate
from ..logic.services import UserService
from fastapi import HTTPException
from typing import List


class UserController:
    def __init__(self):
        self.service = UserService()

    def list_users(self) -> List[User]:
        """Obtiene todos los registros."""
        return ResponseBuilder.success(
            data=users, message="Usuarios obtenidos correctamente"
        )

    # TODO en caso de usar un role distinto  a "user" deberia confirmar medidas de seguridad para limitar acción
    def register_user(self, user: UserCreate):
        profile = self.service.register_user(
            user.email, user.password
        )  # se quita x seguridad -->, user.role
        return ResponseBuilder.success(profile, "Usuario registrado correctamente")

    def delete_user(self, id: str):
        result = self.service.delete_user(id)
        return ResponseBuilder.success(result, "Usuario eliminado correctamente")

    # def get_products(self) -> List[Product]: # "->" Sirve para indicar el tipo de dato que devuelve una función
    #     try:
    #         return self.service.list_products()
    #     except Exception as e:
    #         raise HTTPException(status_code=500, detail=str(e))
    # def get_product_by_id(self, product_id: int) -> Product:
    #     try:
    #         return self.service.get_product(product_id)
    #     except ValueError as ve:
    #         raise HTTPException(status_code=404, detail=str(ve))
    #     except Exception as e:
    #         raise HTTPException(status_code=500, detail=str(e))

    # def create_product(product: ProductCreate):
    #     new_product = self.service.create_product(product.dict())
    #     return new_product
