# app/modules/analytics/api/routes.py
from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, Query

from app.libraries.auth.roles import require_role
from app.libraries.utils.response_models import ApiResponse

from .controller import AnalyticsController
from .schemas import AnalyticsDetail, AnalyticsSummary

router = APIRouter()
controller = AnalyticsController()


@router.get("/summary", response_model=ApiResponse[AnalyticsSummary])
def get_summary(
    company_id: Optional[str] = Query(
        default=None, description="Empresa a la que pertenece el dashboard"
    ),
    current_user=Depends(require_role(["root", "admin", "user"])),
):
    return controller.get_summary(current_user, company_id)


@router.get("/summary/detailed", response_model=ApiResponse[AnalyticsDetail])
def get_detailed_summary(
    company_id: Optional[str] = Query(
        default=None, description="Empresa a la que pertenece el dashboard"
    ),
    current_user=Depends(require_role(["root", "admin", "user"])),
):
    return controller.get_detailed_summary(current_user, company_id)
