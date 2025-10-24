from typing import Union
from fastapi import FastAPI
from app.middleware.error_handler import custom_error_handler
from app.modules.routes import register_routes

app = FastAPI(title="DealerApp API")

# Middlewares
app.middleware("http")(custom_error_handler)

# Registrar todas las rutas de los módulos
register_routes(app)
