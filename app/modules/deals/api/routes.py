# app\modules\deals\api\routes.py
"""Rutas para gestiones."""

from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, Query

from app.libraries.auth.roles import require_role
from app.libraries.utils.response_models import ApiResponse

from .controller import DealController
from .schemas import Deal, DealCreate, DealEmailRequest, DealStatus, DealUpdate

router = APIRouter()
controller = DealController()


@router.get("/", response_model=ApiResponse[List[Deal]])
def list_deals(
    company_id: Optional[str] = Query(default=None),
    advisor_id: Optional[str] = Query(default=None),
    status: Optional[DealStatus] = Query(default=None),
    current_user=Depends(require_role(["root", "admin", "user"])),
):
    return controller.list_deals(
        current_user,
        company_id=company_id,
        advisor_id=advisor_id,
        status=status.value if status else None,
    )


@router.post("/", response_model=ApiResponse[Deal])
def create_deal(
    payload: DealCreate, current_user=Depends(require_role(["root", "admin", "user"]))
):
    return controller.create_deal(current_user, payload)


@router.put("/{deal_id}", response_model=ApiResponse[Deal])
def update_deal(
    deal_id: str,
    payload: DealUpdate,
    current_user=Depends(require_role(["root", "admin", "user"])),
):
    return controller.update_deal(current_user, deal_id, payload)


@router.delete("/{deal_id}")
def delete_deal(
    deal_id: str, current_user=Depends(require_role(["root", "admin", "user"]))
):
    return controller.delete_deal(current_user, deal_id)


@router.post("/{deal_id}/notify", response_model=ApiResponse[dict])
def notify_deal(
    deal_id: str,
    payload: DealEmailRequest,
    current_user=Depends(require_role(["root", "admin"])),
):
    return controller.send_email(current_user, deal_id, payload)


# TODO falto implementar Deals Whatsapp
@router.post("/{deal_id}/whatsapp", response_model=ApiResponse[dict])
def notify_deal_whatsapp(
    deal_id: str,
    payload: DealWhatsAppRequest,
    current_user=Depends(require_role(["root", "admin", "user"])),
):
    return controller.send_whatsapp(current_user, deal_id, payload)
