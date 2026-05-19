"""Layers API endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.models.layer import Layer
from app.schemas.schemas import LayerCreate, LayerResponse

router = APIRouter()

@router.get("/", response_model=list[LayerResponse])
def list_layers(category: str = None, db: Session = Depends(get_db)):
    q = db.query(Layer)
    if category:
        q = q.filter(Layer.category == category)
    return q.order_by(Layer.name).all()

@router.get("/{layer_id}", response_model=LayerResponse)
def get_layer(layer_id: int, db: Session = Depends(get_db)):
    l = db.query(Layer).filter(Layer.id == layer_id).first()
    if not l:
        raise HTTPException(status_code=404, detail="Capa no encontrada")
    return l

@router.post("/", response_model=LayerResponse)
def create_layer(data: LayerCreate, db: Session = Depends(get_db)):
    l = Layer(**data.model_dump(), is_sample=False)
    db.add(l)
    db.commit()
    db.refresh(l)
    return l

@router.put("/{layer_id}", response_model=LayerResponse)
def update_layer(layer_id: int, data: LayerCreate, db: Session = Depends(get_db)):
    l = db.query(Layer).filter(Layer.id == layer_id).first()
    if not l:
        raise HTTPException(status_code=404, detail="Capa no encontrada")
    for k, v in data.model_dump().items():
        setattr(l, k, v)
    db.commit()
    db.refresh(l)
    return l

@router.delete("/{layer_id}")
def delete_layer(layer_id: int, db: Session = Depends(get_db)):
    l = db.query(Layer).filter(Layer.id == layer_id).first()
    if not l:
        raise HTTPException(status_code=404, detail="Capa no encontrada")
    db.delete(l)
    db.commit()
    return {"detail": "Capa eliminada"}
