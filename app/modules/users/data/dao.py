# app/modules/users/data/dao.py
from app.services.supabase_client import supabase


class UserDAO:
    """Capa de acceso a datos de usuarios."""

    def __init__(self):
        self.table = supabase.table("user_profiles")

    def get_all(self):
        return self.table.select("*").execute().data

    def get_by_id(self, user_id: str):
        res = self.table.select("*").eq("id", user_id).execute()
        return res.data[0] if res.data else None

    def get_by_email(self, email: str):
        res = self.table.select("*").eq("email", email).execute()
        return res.data[0] if res.data else None

    def create_profile(self, user_data: dict):
        return self.table.insert(user_data).execute().data[0]

    def update_role_by_email(self, email: str, role: str):
        return (
            self.table.update({"role": role}).eq("email", email).single().execute().data
        )

    def delete_profile(self, user_id: str):
        return self.table.delete().eq("id", user_id).execute()
