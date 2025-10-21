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
            raise Exception(f"[SupabaseDAO:{self.table_name}] Error en '{action}': {str(e)}")

    # --- Métodos CRUD reutilizables ---
    def get_all(self):
        """Obtiene todos los registros de la tabla."""
        response = self.table.select("*").execute()
        return response.data

    def get_by_id(self, record_id: int):
        """Obtiene un registro por su ID."""
        response = self.table.select("*").eq("id", record_id).execute()
        return response.data[0] if response.data else None

    def insert(self, data: dict):
        """Inserta un nuevo registro."""
        response = self.table.insert(data).execute()
        return response.data

    def update(self, record_id: int, data: dict):
        """Actualiza un registro existente por ID."""
        response = self.table.update(data).eq("id", record_id).execute()
        return response.data

    def delete(self, record_id: int):
        """Elimina un registro por ID."""
        response = self.table.delete().eq("id", record_id).execute()
        return response.data

    def filter(self, **filters):
        """Filtra registros por uno o más campos (dinámico)."""
        query = self.table.select("*")
        for key, value in filters.items():
            query = query.eq(key, value)
        response = query.execute()
        return response.data