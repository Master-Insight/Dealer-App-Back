# app/config/settings.py
from pydantic_settings import BaseSettings
from pydantic import Extra

class Settings(BaseSettings):

  # --- DB ---
  SUPABASE_URL: str
  SUPABASE_KEY: str

  class Config:
    env_file = ".env"
    extra = Extra.ignore  # 👈 ignora variables adicionales

# Instancia global
settings = Settings()