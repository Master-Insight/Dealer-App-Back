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
        return ResponseBuilder.success(self.service.list_users())

    def register_user(self, user: UserCreate):
        return ResponseBuilder.success(
            self.service.register_user(user.email, user.password, user.role)
        )

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
