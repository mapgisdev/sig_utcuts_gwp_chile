"""MRV API endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.deps import get_db
from app.models.mrv import MRVIndicator, MRVObservation
from app.schemas.schemas import MRVIndicatorResponse, MRVObservationCreate, MRVObservationResponse

router = APIRouter()

@router.get("/indicators", response_model=list[MRVIndicatorResponse])
def list_indicators(category: str = None, db: Session = Depends(get_db)):
    q = db.query(MRVIndicator)
    if category:
        q = q.filter(MRVIndicator.category == category)
    return q.order_by(MRVIndicator.code).all()

@router.get("/observations", response_model=list[MRVObservationResponse])
def list_observations(intervention_id: int = None, db: Session = Depends(get_db)):
    q = db.query(MRVObservation)
    if intervention_id:
        q = q.filter(MRVObservation.intervention_id == intervention_id)
    return q.all()

@router.post("/observations", response_model=MRVObservationResponse)
def create_observation(data: MRVObservationCreate, db: Session = Depends(get_db)):
    obs = MRVObservation(**data.model_dump(), is_sample=False)
    db.add(obs)
    db.commit()
    db.refresh(obs)
    return obs

@router.put("/observations/{observation_id}", response_model=MRVObservationResponse)
def update_observation(observation_id: int, data: MRVObservationCreate, db: Session = Depends(get_db)):
    obs = db.query(MRVObservation).filter(MRVObservation.id == observation_id).first()
    if not obs:
        raise HTTPException(status_code=404, detail="Observación no encontrada")
    for k, v in data.model_dump().items():
        setattr(obs, k, v)
    db.commit()
    db.refresh(obs)
    return obs

@router.delete("/observations/{observation_id}")
def delete_observation(observation_id: int, db: Session = Depends(get_db)):
    obs = db.query(MRVObservation).filter(MRVObservation.id == observation_id).first()
    if not obs:
        raise HTTPException(status_code=404, detail="Observación no encontrada")
    db.delete(obs)
    db.commit()
    return {"detail": "Observación eliminada"}

@router.get("/summary")
def mrv_summary(db: Session = Depends(get_db)):
    total = db.query(MRVObservation).count()
    verified = db.query(MRVObservation).filter(MRVObservation.verification_status == "verified").count()
    estimated = db.query(MRVObservation).filter(MRVObservation.verification_status == "estimated").count()
    by_cat = db.query(MRVIndicator.category, func.count(MRVObservation.id)).join(
        MRVObservation, MRVObservation.indicator_id == MRVIndicator.id
    ).group_by(MRVIndicator.category).all()
    return {
        "total_observations": total,
        "verified": verified,
        "estimated": estimated,
        "by_category": [{"category": c, "count": n} for c, n in by_cat],
    }
