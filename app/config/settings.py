# app/config/settings.py
from pydantic import Extra
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    # --- DB ---
    SUPABASE_URL: str
    SUPABASE_KEY: str

    # --- Integraciones ---
    RESEND_API_KEY: str | None = None

    # --- Defaults multiempresa ---
    DEFAULT_COMPANY_ID: str | None = None

    class Config:
        env_file = ".env"
        extra = Extra.ignore  # 👈 ignora variables adicionales


# Instancia global
settings = Settings()
