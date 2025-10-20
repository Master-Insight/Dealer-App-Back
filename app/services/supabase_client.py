# app/services/supabase_client.py
from supabase import create_client, Client
from app.config.settings import settings

supabase: Client = create_client(
    settings.SUPABASE_URL,
    settings.SUPABASE_KEY
)