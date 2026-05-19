"""Reports API endpoints."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.deps import get_db
from app.models.investment import Investment
from app.models.project import Project
from app.models.intervention import Intervention
from app.models.mechanism import Mechanism
from app.models.territory import Territory
from app.models.data_quality import DataQualityFlag

router = APIRouter()

@router.get("/national")
def national_report(db: Session = Depends(get_db)):
    total_inv = db.query(func.coalesce(func.sum(Investment.amount_usd), 0)).scalar()
    total_ha_est = db.query(func.coalesce(func.sum(Intervention.hectares_estimated), 0)).scalar()
    total_ha_ver = db.query(func.coalesce(func.sum(Intervention.hectares_verified), 0)).scalar()
    total_co2_est = db.query(func.coalesce(func.sum(Intervention.tco2e_estimated), 0)).scalar()
    return {
        "report_type": "national", "title": "Reporte Nacional UTCUTS Chile",
        "data": {"total_investment_usd": float(total_inv),
                 "mechanisms_count": db.query(Mechanism).count(),
                 "projects_count": db.query(Project).count(),
                 "hectares_estimated": float(total_ha_est),
                 "hectares_verified": float(total_ha_ver),
                 "tco2e_estimated": float(total_co2_est)},
        "note": "Datos demo — no representan información oficial"
    }

@router.get("/data-gaps")
def data_gaps_report(db: Session = Depends(get_db)):
    flags = db.query(DataQualityFlag).filter(DataQualityFlag.resolved == False).all()
    return {
        "report_type": "data_gaps", "title": "Reporte de Brechas de Información",
        "total": len(flags),
        "flags": [{"id": f.id, "entity": f.entity_type, "type": f.flag_type,
                   "severity": f.severity, "description": f.description} for f in flags],
        "note": "Datos demo"
    }

@router.get("/mrv")
def mrv_report(db: Session = Depends(get_db)):
    from app.models.mrv import MRVObservation
    total = db.query(MRVObservation).count()
    verified = db.query(MRVObservation).filter(MRVObservation.verification_status == "verified").count()
    return {
        "report_type": "mrv", "title": "Reporte MRV",
        "total_observations": total, "verified": verified,
        "verification_rate": round(verified / total * 100, 1) if total > 0 else 0,
        "note": "Datos demo"
    }
