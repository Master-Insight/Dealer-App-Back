# app/modules/users/data/dao.py
from app.services.supabase_client import supabase

class UserDAO:
    """Capa de acceso a datos de usuarios."""

    def __init__(self):
        self.table = supabase.table("user_profiles")

    def get_all(self):
        return self.table.select("*").execute().data

    def get_by_email(self, email: str):
        res = self.table.select("*").eq("email", email).execute()
        return res.data[0] if res.data else None

    def create_profile(self, user_data: dict):
        return self.table.insert(user_data).execute().data[0]