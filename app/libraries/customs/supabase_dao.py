# app/libraries/customs/supabase_dao.py
from __future__ import annotations

import logging
from typing import Any, Dict

from postgrest.exceptions import APIError

from app.libraries.exceptions.app_exceptions import DataAccessError
from app.services.supabase_client import supabase

logger = logging.getLogger(__name__)


class CustomSupabaseDAO:
    """
    Clase base genérica para acceder a tablas de Supabase.
    Provee métodos CRUD reutilizables.
    """

    def __init__(self, table_name: str):
        self.table = supabase.table(table_name)
        self.table_name = table_name

    # --- Manejo centralizado de ejecución segura ---
    def _execute(self, query, action: str):
        try:
            response = query.execute()
        except APIError as error:
            logger.exception(
                "Supabase API error during %s on table %s", action, self.table_name
            )
            raise DataAccessError(
                f"Error de Supabase al ejecutar {action}",
                details={"table": self.table_name, "error": error.message},
            ) from error
        except Exception as error:
            logger.exception(
                "Unexpected Supabase error during %s on table %s",
                action,
                self.table_name,
            )
            raise DataAccessError(
                f"Error inesperado al ejecutar {action}",
                details={"table": self.table_name, "error": str(error)},
            ) from error

        if hasattr(response, "error") and response.error:
            logger.error(
                "Supabase response error during %s on table %s: %s",
                action,
                self.table_name,
                response.error.message,
            )
            raise DataAccessError(
                f"Supabase devolvió un error al ejecutar {action}",
                details={
                    "table": self.table_name,
                    "error": response.error.message,
                },
            )

        return response.data

    @staticmethod
    def _extract_single(data: Any) -> Any:
        if isinstance(data, list):
            return data[0] if data else None
        return data

    # --- Métodos CRUD reutilizables ---
    def get_all(self):
        """Obtiene todos los registros de la tabla."""
        query = self.table.select("*")
        return self._execute(query, "get_all")

    def get_by_id(self, record_id: Any):
        """Obtiene un registro por su ID."""
        query = self.table.select("*").eq("id", record_id)
        data = self._execute(query, "get_by_id")
        return data[0] if data else None

    def insert(self, payload: dict):
        """Inserta un nuevo registro y devuelve el registro creado."""
        query = self.table.insert(payload)
        data = self._execute(query, "insert")
        return data[0] if data else None

    def update(self, record_id: Any, payload: dict):
        """Actualiza un registro existente por ID."""
        query = self.table.update(payload).eq("id", record_id)
        data = self._execute(query, "update")
        return data[0] if data else None

    def delete(self, record_id: Any):
        """Elimina un registro por ID."""
        query = self.table.delete().eq("id", record_id)
        data = self._execute(query, "delete")
        if isinstance(data, list):
            return len(data) > 0
        return bool(data)

    def filter(self, **filters):
        """Filtra registros por uno o más campos (dinámico)."""
        query = self.table.select("*")
        for key, value in filters.items():
            query = query.eq(key, value)
        return self._execute(query, "filter")

    def get_first(self, **filters):
        """Obtiene el primer registro que coincide con los filtros dados."""
        data = self.filter(**filters)
        return self._extract_single(data)

    def update_where(self, filters: Dict[str, Any], payload: dict):
        """Actualiza registros que cumplen los filtros y retorna el primero."""
        query = self.table.update(payload)
        for key, value in filters.items():
            query = query.eq(key, value)
        data = self._execute(query, "update_where")
        return self._extract_single(data)
