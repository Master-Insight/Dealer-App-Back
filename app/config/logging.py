# app\config\logging.py
"""Configuración centralizada de logging para la aplicación."""

from __future__ import annotations

import logging
from logging.config import dictConfig
from typing import Any, Dict


LOGGING_CONFIG: Dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        }
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}


def setup_logging() -> None:
    """Inicializa la configuración de logging."""
    dictConfig(LOGGING_CONFIG)
    logging.getLogger(__name__).debug("Logging configurado correctamente")
