"""Dashboard API endpoint."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.deps import get_db
from app.models.mechanism import Mechanism
from app.models.project import Project
from app.models.investment import Investment
from app.models.intervention import Intervention
from app.models.territory import Territory
from app.models.data_quality import DataQualityFlag
from app.models.prioritization import PrioritizationScore
from app.schemas.schemas import DashboardSummary

router = APIRouter()


@router.get("/summary", response_model=DashboardSummary)
def get_dashboard_summary(db: Session = Depends(get_db)):
    total_usd = db.query(func.coalesce(func.sum(Investment.amount_usd), 0)).scalar() or 0
    public = db.query(func.coalesce(func.sum(Investment.amount_usd), 0)).filter(
        Investment.funding_type == "public").scalar() or 0
    private = db.query(func.coalesce(func.sum(Investment.amount_usd), 0)).filter(
        Investment.funding_type == "private").scalar() or 0
    intl = db.query(func.coalesce(func.sum(Investment.amount_usd), 0)).filter(
        Investment.funding_type == "international").scalar() or 0

    est_ha = db.query(func.coalesce(func.sum(Intervention.hectares_estimated), 0)).scalar() or 0
    ver_ha = db.query(func.coalesce(func.sum(Intervention.hectares_verified), 0)).scalar() or 0
    est_co2 = db.query(func.coalesce(func.sum(Intervention.tco2e_estimated), 0)).scalar() or 0
    ver_co2 = db.query(func.coalesce(func.sum(Intervention.tco2e_verified), 0)).scalar() or 0

    # Investment by source
    by_source = db.query(Investment.funding_type, func.sum(Investment.amount_usd)).group_by(
        Investment.funding_type).all()
    inv_by_source = [{"source": s or "Sin clasificar", "amount": float(a or 0)} for s, a in by_source]

    # Investment by intervention type
    by_int = db.query(Intervention.intervention_type, func.sum(Investment.amount_usd)).join(
        Project, Intervention.project_id == Project.id).join(
        Investment, Investment.project_id == Project.id).group_by(
        Intervention.intervention_type).all()
    inv_by_intervention = [{"type": t or "Sin clasificar", "amount": float(a or 0)} for t, a in by_int]

    # Top territories
    top = db.query(PrioritizationScore, Territory.name).join(
        Territory, PrioritizationScore.territory_id == Territory.id).order_by(
        PrioritizationScore.score_total.desc()).limit(5).all()
    top_territories = [{"name": name, "score": float(s.score_total or 0),
                        "priority": s.priority_class} for s, name in top]

    return DashboardSummary(
        total_investment_usd=float(total_usd),
        public_investment_usd=float(public),
        private_investment_usd=float(private),
        international_investment_usd=float(intl),
        mechanisms_count=db.query(Mechanism).count(),
        projects_count=db.query(Project).count(),
        territories_count=db.query(Territory).filter(Territory.type == "commune").count(),
        estimated_hectares=float(est_ha),
        verified_hectares=float(ver_ha),
        estimated_tco2e=float(est_co2),
        verified_tco2e=float(ver_co2),
        data_gaps_count=db.query(DataQualityFlag).filter(DataQualityFlag.resolved == False).count(),
        investment_by_source=inv_by_source,
        investment_by_intervention=inv_by_intervention,
        top_territories=top_territories,
    )
