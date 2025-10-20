from typing import Union
from fastapi import FastAPI
from app.modules.routes import register_routes

app = FastAPI(title="DealerApp API")

# Registrar todas las rutas de los módulos
register_routes(app)