# app/libraries/customs/base_service.py
"""Capa base para encapsular operaciones comunes de los servicios."""

from __future__ import annotations

import logging
from typing import Any, Dict

from app.libraries.exceptions.app_exceptions import (
    AppError,
    NotFoundError,
    ServiceError,
)


class BaseService:
    """Clase base reutilizable para las operaciones de negocio."""

    def __init__(self, dao):
        self.dao = dao
        self.logger = logging.getLogger(
            f"{self.__class__.__module__}.{self.__class__.__name__}"
        )

    def list_all(self):
        """Devuelve todos los registros."""
        try:
            return self.dao.get_all()
        except AppError:
            raise
        except Exception as exc:
            self.logger.exception("Error inesperado al listar registros")
            raise ServiceError(details={"error": str(exc)}) from exc

    def get_by_id(self, record_id: Any):
        """Devuelve un registro por su ID."""
        try:
            record = self.dao.get_by_id(record_id)
            if not record:
                raise NotFoundError(
                    message=f"Registro con ID {record_id} no encontrado",
                    details={"id": record_id},
                )
            return record
        except AppError:
            raise
        except Exception as exc:
            self.logger.exception(
                "Error inesperado al obtener el registro con ID %s", record_id
            )
            raise ServiceError(
                message="Error al obtener registro",
                details={"id": record_id, "error": str(exc)},
            ) from exc

    def create(self, data: Dict[str, Any]):
        """Crea un nuevo registro."""
        try:
            return self.dao.insert(data)
        except AppError:
            raise
        except Exception as exc:
            self.logger.exception("Error inesperado al crear registro")
            raise ServiceError(
                message="Error al crear registro", details={"error": str(exc)}
            ) from exc

    def update(self, record_id: Any, data: Dict[str, Any]):
        """Actualiza un registro existente."""
        try:
            updated = self.dao.update(record_id, data)
            if not updated:
                raise NotFoundError(
                    message=f"Registro con ID {record_id} no encontrado",
                    details={"id": record_id},
                )
            return updated
        except AppError:
            raise
        except Exception as exc:
            self.logger.exception(
                "Error inesperado al actualizar el registro con ID %s", record_id
            )
            raise ServiceError(
                message="Error al actualizar registro",
                details={"id": record_id, "error": str(exc)},
            ) from exc

    def delete(self, record_id: Any):
        """Elimina un registro existente."""
        try:
            deleted = self.dao.delete(record_id)
            if not deleted:
                raise NotFoundError(
                    message=f"Registro con ID {record_id} no encontrado",
                    details={"id": record_id},
                )
            return {
                "deleted": True,
                "id": record_id,
                "message": f"Registro {record_id} eliminado correctamente",
            }
        except AppError:
            raise
        except Exception as exc:
            self.logger.exception(
                "Error inesperado al eliminar el registro con ID %s", record_id
            )
            raise ServiceError(
                message="Error al eliminar registro",
                details={"id": record_id, "error": str(exc)},
            ) from exc
