"""Evidence upload API endpoint."""
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.models.evidence import EvidenceFile

router = APIRouter()

@router.post("/upload")
def upload_evidence(entity_type: str = "project", entity_id: int = 0,
                    file: UploadFile = File(...), db: Session = Depends(get_db)):
    ev = EvidenceFile(filename=file.filename, original_name=file.filename,
                      file_type=file.content_type, entity_type=entity_type,
                      entity_id=entity_id, file_path=f"/data/evidence/{file.filename}")
    db.add(ev)
    db.commit()
    db.refresh(ev)
    return {"id": ev.id, "filename": ev.filename, "message": "Evidencia registrada"}

@router.get("/{evidence_id}")
def get_evidence(evidence_id: int, db: Session = Depends(get_db)):
    ev = db.query(EvidenceFile).filter(EvidenceFile.id == evidence_id).first()
    if not ev:
        raise HTTPException(status_code=404, detail="Evidencia no encontrada")
    return {"id": ev.id, "filename": ev.filename, "type": ev.file_type,
            "entity_type": ev.entity_type, "entity_id": ev.entity_id}
