# app\modules\clients\data\dao.py
"""DAO para clientes."""

from __future__ import annotations

from app.libraries.customs.supabase_dao import CustomSupabaseDAO


class ClientDAO(CustomSupabaseDAO):
    """Acceso a datos para la tabla `clients`."""

    def __init__(self) -> None:
        super().__init__("clients")

    def search(self, *, company_id: str, term: str):
        """Búsqueda simple por email, teléfono o DNI."""

        query = self._build_select_query().eq("company_id", company_id)
        query = query.or_(
            f"email.ilike.%{term}%,phone.ilike.%{term}%,dni.ilike.%{term}%"
        )
        return self._execute(query, "search")
