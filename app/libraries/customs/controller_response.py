# app/libraries/customs/controller_base.py
from fastapi import HTTPException
from typing import TypeVar, Generic, List, Optional, Any, Dict, Type

from app.libraries.utils.response_builder import ResponseBuilder

T = TypeVar("T")  # Modelo de salida (por ejemplo, Product)
C = TypeVar("C")  # Modelo de creación (por ejemplo, ProductCreate)


class ResponseController(Generic[T, C]):
    """
    Controlador genérico con manejo estándar de errores y operaciones CRUD básicas.
    Los controladores específicos (como ProductController) heredan de esta clase.
    """

    def __init__(self, service: Any):
        self.service = service

    def list_all(self) -> List[T]:
        """Obtiene todos los registros."""
        return ResponseBuilder.success(self.service.list_all())

    def get_by_id(self, item_id: int) -> Optional[T]:
        """Obtiene un registro por ID."""
        item = self.service.get_by_id(item_id)
        if not item:
            raise HTTPException(
                status_code=404, detail=f"Registro con ID {item_id} no encontrado"
            )
        return ResponseBuilder.success(item)

    def create(self, data: C) -> T:
        """Crea un nuevo registro."""
        return ResponseBuilder.success(self.service.create(data.dict()))

    def update(self, item_id: int, data: Dict[str, Any]) -> T:
        """Actualiza un registro existente."""
        updated = self.service.update(item_id, data)
        if not updated:
            raise HTTPException(
                status_code=404, detail=f"Registro con ID {item_id} no encontrado"
            )
        return ResponseBuilder.success(updated)

    def delete(self, item_id: int) -> Dict[str, Any]:
        """Elimina un registro."""
        success = self.service.delete(item_id)
        if not success:
            raise HTTPException(
                status_code=404, detail=f"Registro con ID {item_id} no encontrado"
            )
        return ResponseBuilder.success(f"Registro {item_id} eliminado correctamente")
