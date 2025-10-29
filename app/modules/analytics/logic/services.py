# app\modules\analytics\logic\services.py
from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from typing import Dict, Iterable, List, Optional

from app.config.settings import settings
from app.libraries.exceptions.app_exceptions import AuthError, ValidationError

from ...clients.data.dao import ClientDAO
from ...deals.data.dao import DealDAO
from ...products.data.dao import ProductDAO


class AnalyticsService:
    """Genera dashboards operativos para compañías y asesores."""

    def __init__(self) -> None:
        self.deal_dao = DealDAO()
        self.product_dao = ProductDAO()
        self.client_dao = ClientDAO()

    # ------------------------------------------------------------------
    # Métodos públicos
    # ------------------------------------------------------------------
    def build_summary(
        self, profile: Dict, company_id: Optional[str]
    ) -> Dict[str, object]:
        company = self._resolve_company(profile, company_id)
        advisor_filter = profile.get("role") == "user"

        deals = self._get_deals(company, advisor_filter, profile)
        products = self.product_dao.filter(company_id=company)
        clients = self.client_dao.filter(company_id=company)

        return self._compose_summary(
            company=company,
            deals=deals,
            products=products,
            clients=clients,
            advisor_filter=advisor_filter,
        )

    def build_detailed_summary(
        self, profile: Dict, company_id: Optional[str]
    ) -> Dict[str, object]:
        summary = self.build_summary(profile, company_id)

        company = summary["company_id"]
        advisor_filter = summary["advisor_filter_applied"]
        profile_id = profile.get("id") if advisor_filter else None

        activity_trend = self._build_activity_trend(company, profile_id)
        summary["activity_trend"] = activity_trend
        return summary

    # ------------------------------------------------------------------
    # Helpers internos
    # ------------------------------------------------------------------
    def _resolve_company(self, profile: Dict, company_id: Optional[str]) -> str:
        if profile.get("role") == "root" and company_id:
            return company_id

        target = company_id or profile.get("company_id") or settings.DEFAULT_COMPANY_ID
        if not target:
            raise ValidationError(
                "No se puede generar el dashboard sin especificar una compañía"
            )

        if (
            profile.get("role") == "admin"
            and company_id
            and company_id != profile.get("company_id")
        ):
            raise AuthError("No puedes consultar datos de otra empresa")

        if profile.get("role") == "user" and target != profile.get("company_id"):
            raise AuthError("No tienes permiso para consultar otra empresa")

        return target

    def _get_deals(
        self, company_id: str, advisor_filter: bool, profile: Dict
    ) -> List[Dict]:
        filters = {"company_id": company_id}
        if advisor_filter:
            filters["advisor_id"] = profile.get("id")
        return self.deal_dao.filter_by(filters)

    def _compose_summary(
        self,
        *,
        company: str,
        deals: List[Dict],
        products: List[Dict],
        clients: List[Dict],
        advisor_filter: bool,
    ) -> Dict[str, object]:
        deals_counter = Counter((deal.get("status") or "desconocido") for deal in deals)

        total_deals = sum(deals_counter.values())
        closed_deals = deals_counter.get("realizada", 0)
        conversion_rate = (
            round((closed_deals / total_deals) * 100, 2) if total_deals else 0.0
        )

        upcoming = self._count_upcoming_deals(deals)

        product_counter = Counter(
            (product.get("status") or "desconocido") for product in products
        )

        recent_clients = self._count_recent_clients(clients)

        generated_at = datetime.now(timezone.utc)

        return {
            "company_id": company,
            "generated_at": generated_at,
            "advisor_filter_applied": advisor_filter,
            "deals": {
                "total": total_deals,
                "by_status": dict(deals_counter),
                "conversion_rate": conversion_rate,
                "upcoming_next_7_days": upcoming,
            },
            "products": {
                "total": len(products),
                "by_status": dict(product_counter),
            },
            "clients": {
                "total": len(clients),
                "new_last_30_days": recent_clients,
            },
        }

    def _count_upcoming_deals(self, deals: Iterable[Dict]) -> int:
        now = datetime.now(timezone.utc)
        limit = now + timedelta(days=7)
        count = 0

        for deal in deals:
            scheduled = deal.get("scheduled_for")
            if not scheduled:
                continue

            parsed = self._parse_datetime(scheduled)
            if parsed and now <= parsed <= limit:
                count += 1

        return count

    def _count_recent_clients(self, clients: Iterable[Dict]) -> int:
        threshold = datetime.now(timezone.utc) - timedelta(days=30)
        count = 0
        for client in clients:
            created_at = client.get("created_at")
            parsed = self._parse_datetime(created_at)
            if parsed and parsed >= threshold:
                count += 1
        return count

    def _build_activity_trend(
        self, company_id: str, advisor_id: Optional[str]
    ) -> List[Dict[str, object]]:
        days = 14
        start = datetime.now(timezone.utc) - timedelta(days=days)
        deals = self.deal_dao.filter_by({"company_id": company_id})
        clients = self.client_dao.filter(company_id=company_id)

        deal_counts = defaultdict(int)
        for deal in deals:
            if advisor_id and deal.get("advisor_id") != advisor_id:
                continue
            created_at = self._parse_datetime(deal.get("created_at"))
            if created_at and created_at >= start:
                deal_counts[created_at.date()] += 1

        client_counts = defaultdict(int)
        for client in clients:
            created_at = self._parse_datetime(client.get("created_at"))
            if created_at and created_at >= start:
                client_counts[created_at.date()] += 1

        trend: List[Dict[str, object]] = []
        for i in range(days + 1):
            day = (start + timedelta(days=i)).date()
            trend.append(
                {
                    "date": datetime.combine(
                        day, datetime.min.time(), tzinfo=timezone.utc
                    ),
                    "deals_created": deal_counts.get(day, 0),
                    "new_clients": client_counts.get(day, 0),
                }
            )

        return trend

    @staticmethod
    def _parse_datetime(value: Optional[object]) -> Optional[datetime]:
        if isinstance(value, datetime):
            return value if value.tzinfo else value.replace(tzinfo=timezone.utc)

        if not value:
            return None

        text = str(value)
        text = text.replace("Z", "")

        try:
            parsed = datetime.fromisoformat(text)
            return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)
        except ValueError:
            return None
