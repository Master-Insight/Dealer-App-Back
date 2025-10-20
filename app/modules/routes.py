# app/modules/routes.py
from fastapi import FastAPI
# from app.modules.presales.router import router as presales_router
# from app.modules.products.router import router as products_router
# from app.modules.users.router import router as users_router

def register_routes(app: FastAPI):
    # --- Ruta base ---
    @app.get("/")
    def read_root():
        return {"message": "DealerApp API funcionando correctamente 🚗"}

    # --- Rutas de módulos ---
    # app.include_router(presales_router, prefix="/presales", tags=["Presales"])
    # app.include_router(products_router, prefix="/products", tags=["Products"])
    # app.include_router(users_router, prefix="/users", tags=["Users"])