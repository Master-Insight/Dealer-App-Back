# app/libraries/customs/supabase_dao.py
from app.services.supabase_client import supabase


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
            if hasattr(response, "error") and response.error:
                raise Exception(response.error.message)
            return response.data
        except Exception as e:
            raise Exception(
                f"[SupabaseDAO:{self.table_name}] Error en '{action}': {str(e)}"
            )

    # --- Métodos CRUD reutilizables ---
    def get_all(self):
        """Obtiene todos los registros de la tabla."""
        query = self.table.select("*")
        return self._execute(query, "get_all")

    def get_by_id(self, record_id: int):
        """Obtiene un registro por su ID."""
        query = self.table.select("*").eq("id", record_id)
        data = self._execute(query, "get_by_id")
        return data[0] if data else None

    def insert(self, payload: dict):
        """Inserta un nuevo registro y devuelve el registro creado."""
        query = self.table.insert(payload)
        data = self._execute(query, "insert")
        return data[0] if data else None

    def update(self, record_id: int, payload: dict):
        """Actualiza un registro existente por ID."""
        query = self.table.update(payload).eq("id", record_id)
        data = self._execute(query, "update")
        return data[0] if data else None

    def delete(self, record_id: int):
        """Elimina un registro por ID."""
        query = self.table.delete().eq("id", record_id)
        return self._execute(query, "delete")

    def filter(self, **filters):
        """Filtra registros por uno o más campos (dinámico)."""
        query = self.table.select("*")
        for key, value in filters.items():
            query = query.eq(key, value)
        return self._execute(query, "filter")
