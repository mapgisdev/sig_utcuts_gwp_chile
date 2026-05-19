"""Interventions API endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.models.intervention import Intervention
from app.schemas.schemas import InterventionCreate, InterventionResponse

router = APIRouter()

@router.get("/", response_model=list[InterventionResponse])
def list_interventions(project_id: int = None, type: str = None, db: Session = Depends(get_db)):
    q = db.query(Intervention)
    if project_id:
        q = q.filter(Intervention.project_id == project_id)
    if type:
        q = q.filter(Intervention.intervention_type == type)
    return q.all()

@router.get("/{intervention_id}", response_model=InterventionResponse)
def get_intervention(intervention_id: int, db: Session = Depends(get_db)):
    i = db.query(Intervention).filter(Intervention.id == intervention_id).first()
    if not i:
        raise HTTPException(status_code=404, detail="Intervención no encontrada")
    return i

@router.post("/", response_model=InterventionResponse)
def create_intervention(data: InterventionCreate, db: Session = Depends(get_db)):
    i = Intervention(**data.model_dump(), is_sample=False)
    db.add(i)
    db.commit()
    db.refresh(i)
    return i

@router.delete("/{intervention_id}")
def delete_intervention(intervention_id: int, db: Session = Depends(get_db)):
    i = db.query(Intervention).filter(Intervention.id == intervention_id).first()
    if not i:
        raise HTTPException(status_code=404, detail="Intervención no encontrada")
    db.delete(i)
    db.commit()
    return {"detail": "Intervención eliminada"}

@router.put("/{intervention_id}", response_model=InterventionResponse)
def update_intervention(intervention_id: int, data: InterventionCreate, db: Session = Depends(get_db)):
    i = db.query(Intervention).filter(Intervention.id == intervention_id).first()
    if not i:
        raise HTTPException(status_code=404, detail="Intervención no encontrada")
    for k, v in data.model_dump().items():
        setattr(i, k, v)
    db.commit()
    db.refresh(i)
    return i
