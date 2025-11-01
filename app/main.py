from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.logging import setup_logging
from app.middleware.error_handler import custom_error_handler
from app.modules.routes import register_routes
from app.middleware.request_context import RequestContextLogMiddleware

setup_logging()

app = FastAPI(title="DealerApp API")

# 🔹 Lista de orígenes permitidos
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Permite GET, POST, PUT, DELETE, OPTIONS, etc.
    allow_headers=["*"],  # Permite headers personalizados como Authorization
)

# Middlewares
app.middleware("http")(custom_error_handler)
app.add_middleware(RequestContextLogMiddleware)

# Registrar todas las rutas de los módulos
register_routes(app)
