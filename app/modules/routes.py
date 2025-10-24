# app/modules/routes.py
from fastapi import FastAPI, Depends

# from app.modules.presales.api.routes import router as presales_router
from app.libraries.utils.response_builder import ResponseBuilder
from app.modules.products.api.routes import router as products_router
from app.modules.users.api.routes import router as users_router
from app.libraries.auth.dependencies import get_current_user


def register_routes(app: FastAPI):
    # --- Ruta base ---
    @app.get("/")
    def read_root():
        return ResponseBuilder.success("DealerApp API funcionando correctamente 🚗")

    # --- Ruta test usaurio ---
    @app.get("/me")
    def get_profile(current_user=Depends(get_current_user)):
        return current_user

    # --- Rutas de módulos ---
    # app.include_router(presales_router, prefix="/presales", tags=["Presales"])
    app.include_router(products_router, prefix="/products", tags=["Products"])
    app.include_router(users_router, prefix="/users", tags=["Users"])
