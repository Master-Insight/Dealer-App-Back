# app/modules/routes.py
from fastapi import FastAPI, Depends

# from app.modules.presales.api.routes import router as presales_router
from app.libraries.utils.response_builder import ResponseBuilder
from app.modules.products.api.routes import router as products_router
from app.modules.users.api.routes import router as users_router

from app.modules.test.routes import router as test_router


def register_routes(app: FastAPI):
    # --- Ruta base ---
    @app.get("/")
    def read_root():
        return ResponseBuilder.success("DealerApp API funcionando correctamente 🚗")

    # --- Rutas de módulos ---
    # app.include_router(presales_router, prefix="/presales", tags=["Presales"])
    app.include_router(products_router, prefix="/products", tags=["Products"])
    app.include_router(users_router, prefix="/users", tags=["Users"])

    app.include_router(test_router, prefix="/test")
