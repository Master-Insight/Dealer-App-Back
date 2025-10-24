# app/middleware/error_handler.py
from fastapi import Request
from fastapi.responses import JSONResponse
from app.libraries.utils.response_builder import ResponseBuilder


async def custom_error_handler(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        # Si ya es HTTPException, la dejamos pasar
        if hasattr(e, "status_code"):
            content = getattr(e, "detail", str(e))
            return JSONResponse(status_code=e.status_code, content=content)

        # Si es otra excepción, la normalizamos
        error = ResponseBuilder.error("Error interno del servidor", str(e), 500)

        # No levantamos, devolvemos la respuesta directamente
        return JSONResponse(status_code=500, content=error)
