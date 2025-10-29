# app/modules/quotations/api/routes.py
from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, Query

from app.libraries.auth.roles import require_role
from app.libraries.utils.response_models import ApiResponse

from .controller import QuotationController
from .schemas import Quotation, QuotationCreate, QuotationUpdate

router = APIRouter()
controller = QuotationController()


@router.get("/", response_model=ApiResponse[List[Quotation]])
def list_quotations(
    company_id: Optional[str] = Query(default=None),
    deal_id: Optional[str] = Query(default=None),
    current_user=Depends(require_role(["root", "admin", "user"])),
):
    return controller.list_quotations(current_user, company_id, deal_id)


@router.post("/", response_model=ApiResponse[Quotation])
def create_quotation(
    payload: QuotationCreate,
    current_user=Depends(require_role(["root", "admin", "user"])),
):
    return controller.create_quotation(current_user, payload)


@router.put("/{quotation_id}", response_model=ApiResponse[Quotation])
def update_quotation(
    quotation_id: str,
    payload: QuotationUpdate,
    current_user=Depends(require_role(["root", "admin", "user"])),
):
    return controller.update_quotation(current_user, quotation_id, payload)


@router.delete("/{quotation_id}")
def delete_quotation(
    quotation_id: str,
    current_user=Depends(require_role(["root", "admin"])),
):
    return controller.delete_quotation(current_user, quotation_id)
