# app/services/supabase_client.py
from supabase import create_client, Client
from app.config.settings import settings

url: str = settings.SUPABASE_URL
key: str = settings.SUPABASE_KEY

supabase: Client = create_client(url, key)