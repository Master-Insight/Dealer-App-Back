# app\modules\clients\api\routes.py
"""Rutas de clientes."""

from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, Query

from app.libraries.auth.roles import require_role
from app.libraries.utils.response_models import ApiResponse

from .controller import ClientController
from .schemas import Client, ClientCreate, ClientUpdate

router = APIRouter()
controller = ClientController()


@router.get("/", response_model=ApiResponse[List[Client]])
def list_clients(
    company_id: Optional[str] = Query(
        default=None, description="Filtrar clientes por empresa"
    ),
    current_user=Depends(require_role(["root", "admin", "user"])),
):
    return controller.list_clients(current_user, company_id)


@router.get("/search", response_model=ApiResponse[List[Client]])
def search_clients(
    term: str = Query(..., description="Texto a buscar en email/teléfono/DNI"),
    current_user=Depends(require_role(["root", "admin", "user"])),
):
    return controller.search_clients(current_user, term)


@router.post("/", response_model=ApiResponse[Client])
def create_client(
    payload: ClientCreate, current_user=Depends(require_role(["root", "admin", "user"]))
):
    return controller.create_client(current_user, payload)


@router.put("/{client_id}", response_model=ApiResponse[Client])
def update_client(
    client_id: str,
    payload: ClientUpdate,
    current_user=Depends(require_role(["root", "admin", "user"])),
):
    return controller.update_client(current_user, client_id, payload)


@router.delete("/{client_id}")
def delete_client(
    client_id: str, current_user=Depends(require_role(["root", "admin", "user"]))
):
    return controller.delete_client(current_user, client_id)
