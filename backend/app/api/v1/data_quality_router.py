"""Data Quality / Gaps API endpoints."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.deps import get_db
from app.models.data_quality import DataQualityFlag
from app.schemas.schemas import DataQualityFlagResponse

router = APIRouter()

@router.get("/flags", response_model=list[DataQualityFlagResponse])
def list_flags(entity_type: str = None, resolved: bool = None, db: Session = Depends(get_db)):
    q = db.query(DataQualityFlag)
    if entity_type:
        q = q.filter(DataQualityFlag.entity_type == entity_type)
    if resolved is not None:
        q = q.filter(DataQualityFlag.resolved == resolved)
    return q.order_by(DataQualityFlag.created_at.desc()).all()

@router.get("/summary")
def data_quality_summary(db: Session = Depends(get_db)):
    total = db.query(DataQualityFlag).filter(DataQualityFlag.resolved == False).count()
    by_type = db.query(DataQualityFlag.flag_type, func.count(DataQualityFlag.id)
                       ).filter(DataQualityFlag.resolved == False
                       ).group_by(DataQualityFlag.flag_type).all()
    by_severity = db.query(DataQualityFlag.severity, func.count(DataQualityFlag.id)
                           ).filter(DataQualityFlag.resolved == False
                           ).group_by(DataQualityFlag.severity).all()
    by_entity = db.query(DataQualityFlag.entity_type, func.count(DataQualityFlag.id)
                         ).filter(DataQualityFlag.resolved == False
                         ).group_by(DataQualityFlag.entity_type).all()
    return {
        "total_unresolved": total,
        "by_type": [{"type": t, "count": c} for t, c in by_type],
        "by_severity": [{"severity": s, "count": c} for s, c in by_severity],
        "by_entity": [{"entity": e, "count": c} for e, c in by_entity],
    }

@router.put("/flags/{flag_id}/resolve")
def resolve_flag(flag_id: int, db: Session = Depends(get_db)):
    from datetime import datetime
    flag = db.query(DataQualityFlag).filter(DataQualityFlag.id == flag_id).first()
    if not flag:
        return {"detail": "Flag no encontrado"}
    flag.resolved = True
    flag.resolved_at = datetime.utcnow()
    db.commit()
    return {"detail": "Flag resuelto"}
