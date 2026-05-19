"""Kobo / XLSForm API Router — manages Kobo configurations, staging, and dynamic ingestion."""
import json
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, Dict, Any, List

from app.core.deps import get_db
from app.services import xlsform_parser
from app.models.kobo import KoboConfig, KoboStagingRecord

# Import all target models to perform ingestion insertions
from app.models.mechanism import Mechanism
from app.models.project import Project
from app.models.investment import Investment
from app.models.intervention import Intervention
from app.models.mrv import MRVObservation, MRVIndicator
from app.models.layer import Layer
from app.models.territory import Territory

router = APIRouter()

# --- Pydantic Schemas ---
class KoboConfigCreate(BaseModel):
    form_id: str
    form_name: str
    kobo_asset_id: Optional[str] = None
    kobo_url: Optional[str] = "https://kf.kobotoolbox.org/api/v2/assets/"
    api_token: Optional[str] = None
    target_model: Optional[str] = None
    auto_sync: Optional[bool] = False

class SimulateSyncRequest(BaseModel):
    filename: str
    payload: Dict[str, Any]

# --- API Endpoints ---

@router.get("/forms")
def list_xlsforms():
    """Scans and lists all XLSForms detected inside the insumos/formularios_xlsform directory."""
    return xlsform_parser.scan_xlsforms()

@router.get("/forms/{filename}")
def get_xlsform_details(filename: str):
    """Compiles and returns the survey structure, conditions, and choices for a selected XLSForm."""
    try:
        return xlsform_parser.parse_xlsform(filename)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error compiling XLSForm structure: {str(e)}")

@router.get("/configs")
def list_kobo_configs(db: Session = Depends(get_db)):
    """Retrieves all KoboToolbox configurations."""
    return db.query(KoboConfig).all()

@router.post("/configs")
def save_kobo_config(config: KoboConfigCreate, db: Session = Depends(get_db)):
    """Saves or updates a Kobo form connection mapping configuration."""
    existing = db.query(KoboConfig).filter(KoboConfig.form_id == config.form_id).first()
    if existing:
        for k, v in config.model_dump().items():
            setattr(existing, k, v)
        db.commit()
        db.refresh(existing)
        return existing
    
    new_config = KoboConfig(**config.model_dump())
    db.add(new_config)
    db.commit()
    db.refresh(new_config)
    return new_config

@router.get("/staging/records")
def list_staging_records(
    form_id: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Lists staging area records with filter parameters."""
    q = db.query(KoboStagingRecord)
    if form_id:
        q = q.filter(KoboStagingRecord.form_id == form_id)
    if status:
        q = q.filter(KoboStagingRecord.status == status)
    return q.order_by(KoboStagingRecord.created_at.desc()).all()

@router.post("/staging/simulate-sync")
def simulate_xlsform_sync(req: SimulateSyncRequest, db: Session = Depends(get_db)):
    """Simulates an ingestion push.

    Parses payload against XLSForm schema, runs required/range validation
    rules, stores transaction in KoboStagingRecord, and if clean, updates the
    production system table.
    """
    try:
        form_meta = xlsform_parser.parse_xlsform(req.filename)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Could not load XLSForm metadata: {e}")
    
    payload = req.payload
    validation_errors = []
    
    # 1. Run XLSForm structural rules (Required, Constraints, Relevant dependency evaluation)
    for field in form_meta.get("fields", []):
        field_type = field.get("type", "")
        field_name = field.get("name", "")
        field_label = field.get("label", field_name)
        is_required = field.get("required", False)
        relevant_rule = field.get("relevant")
        constraint_rule = field.get("constraint")
        
        # Skip groups and structural labels
        if field_type in ("begin_group", "end_group", "begin_repeat", "end_repeat", "note"):
            continue
            
        field_val = payload.get(field_name)
        
        # A. Evaluation of relevance visibility dependencies (relevant condition)
        # Dynamic check of typical XLSForm conditions (e.g. ${variable} = 'value')
        is_relevant = True
        if relevant_rule:
            is_relevant = False
            try:
                # Basic parser for relevant rules e.g. ${tipo_intervencion} = 'restauracion'
                for ref_var in payload.keys():
                    token = f"${{{ref_var}}}"
                    if token in relevant_rule:
                        ref_val = payload[ref_var]
                        # Replace token with literal Python representation for evaluation
                        relevant_rule = relevant_rule.replace(token, repr(ref_val))
                
                # Replace single = with double == if needed
                eval_expr = relevant_rule.replace(" = ", " == ").replace(" and ", " and ").replace(" or ", " or ")
                is_relevant = eval(eval_expr)
            except Exception as eval_err:
                # Fallback to keep evaluating if parsing error occurs
                is_relevant = True
                
        # If the field is not relevant, it's not required or subject to constraints
        if not is_relevant:
            continue
            
        # B. Check required values
        if is_required and (field_val is None or str(field_val).strip() == ""):
            validation_errors.append({
                "field": field_name,
                "label": field_label,
                "error": "Este campo es requerido por el formulario XLSForm."
            })
            continue
            
        # C. Check range constraints (constraint check)
        if field_val is not None and str(field_val).strip() != "" and constraint_rule:
            try:
                # Evaluate numeric range rules like . > 0 or . <= 100
                cleaned_val = float(field_val) if field_type in ("integer", "decimal") else field_val
                eval_expr = constraint_rule.replace(".", repr(cleaned_val)).replace(" = ", " == ")
                if not eval(eval_expr):
                    validation_errors.append({
                        "field": field_name,
                        "label": field_label,
                        "error": field.get("constraint_message") or f"El valor '{field_val}' no cumple con la regla XLSForm: {constraint_rule}"
                    })
            except Exception:
                pass # skip evaluation error
                
    # 2. Save staging record
    status = "failed" if validation_errors else "validated"
    
    staging_rec = KoboStagingRecord(
        form_id=form_meta["form_id"],
        kobo_uuid=payload.get("_uuid") or f"sim-{datetime.utcnow().timestamp()}",
        payload_json=json.dumps(payload),
        status=status,
        validation_errors=json.dumps(validation_errors) if validation_errors else None
    )
    db.add(staging_rec)
    db.flush()
    
    # 3. Map staging keys directly into main system production models (NATIVE INGESTION)
    imported_id = None
    if not validation_errors:
        try:
            # 1. SPECIAL CASE: Project + Investment Joint Ingestion (from 02_registro_inversiones_proyectos.xlsx)
            if req.filename == "02_registro_inversiones_proyectos.xlsx":
                # Create Project
                proj_attrs = {
                    "name": payload.get("nombre_proyecto") or "Nuevo Proyecto XLSForm",
                    "description": payload.get("descripcion_proyecto") or "Ingresado directamente desde el formulario nativo.",
                    "start_year": int(payload.get("anio_inicio")) if payload.get("anio_inicio") else 2026,
                    "end_year": int(payload.get("anio_fin")) if payload.get("anio_fin") else 2030,
                    "source_reference": payload.get("referencia_fuente") or "Formulario Operativo",
                    "data_confidence": payload.get("nivel_confianza") or "medium"
                }
                
                # Fetch first mechanism in DB to link project
                first_mech = db.query(Mechanism).first()
                proj_attrs["mechanism_id"] = first_mech.id if first_mech else 1
                
                new_project = Project(**proj_attrs)
                db.add(new_project)
                db.flush()
                
                # Create linked Investment
                inv_attrs = {
                    "project_id": new_project.id,
                    "funding_source": payload.get("fuente_financiamiento") or "Inversión Directa Operativa",
                    "funding_type": payload.get("tipo_financiamiento") or "mixed",
                    "amount": float(payload.get("monto_inversion")) if payload.get("monto_inversion") else 100000.0,
                    "amount_usd": float(payload.get("monto_usd")) if payload.get("monto_usd") else 100000.0,
                    "year": int(payload.get("anio_inversion")) if payload.get("anio_inversion") else 2026,
                    "financial_instrument": payload.get("instrumento_financiero") or "Aporte Directo",
                    "approved_amount": float(payload.get("monto_aprobado")) if payload.get("monto_aprobado") else 100000.0,
                    "executed_amount": float(payload.get("monto_ejecutado")) if payload.get("monto_ejecutado") else 100000.0,
                    "committed_amount": float(payload.get("monto_comprometido")) if payload.get("monto_comprometido") else 100000.0,
                    "source_document": payload.get("documento_fuente") or "Direct Submission",
                    "data_quality": payload.get("calidad_dato") or "official"
                }
                new_investment = Investment(**inv_attrs)
                db.add(new_investment)
                db.flush()
                
                staging_rec.status = "imported"
                staging_rec.imported_entity_id = new_project.id
                imported_id = new_project.id
                
            # 2. Case: Mechanisms Ingestion (01_catalogo_mecanismos.xlsx)
            elif req.filename == "01_catalogo_mecanismos.xlsx":
                mech_attrs = {
                    "code": payload.get("codigo_mecanismo") or f"MEC-{datetime.utcnow().timestamp()}",
                    "name": payload.get("nombre_mecanismo") or "Mecanismo Ingestado",
                    "category": payload.get("categoria_mecanismo") or "legal",
                    "description": payload.get("descripcion_mecanismo") or "Creado nativamente.",
                    "main_funding_source": payload.get("fuente_principal") or "Presupuesto",
                    "time_horizon": payload.get("horizonte_temporal") or "medium",
                    "maturity_level": payload.get("estado_madurez") or "concept",
                    "ndc_alignment": payload.get("alineacion_ndc") or "Mitigación",
                    "target_beneficiaries": payload.get("beneficiarios_objetivo") or "Público",
                    "status": payload.get("estado_registro") or "activo"
                }
                new_mech = Mechanism(**mech_attrs)
                db.add(new_mech)
                db.flush()
                
                staging_rec.status = "imported"
                staging_rec.imported_entity_id = new_mech.id
                imported_id = new_mech.id
                
            # 3. Case: Interventions Ingestion (03_intervenciones_utcuts_geometria.xlsx)
            elif req.filename == "03_intervenciones_utcuts_geometria.xlsx":
                # Find project to link
                entered_proj_id = payload.get("proyecto_id")
                target_proj = db.query(Project).filter(Project.id == entered_proj_id).first() if entered_proj_id else None
                if not target_proj:
                    target_proj = db.query(Project).first()
                    
                inter_attrs = {
                    "project_id": target_proj.id if target_proj else 1,
                    "intervention_type": payload.get("tipo_intervencion") or "restauracion",
                    "ndc_component": payload.get("componente_ndc") or "Mitigación",
                    "hectares_estimated": float(payload.get("hectareas_estimadas")) if payload.get("hectareas_estimadas") else 10.0,
                    "hectares_verified": float(payload.get("hectareas_verificadas")) if payload.get("hectareas_verificadas") else 10.0,
                    "tco2e_estimated": float(payload.get("tco2_estimado")) if payload.get("tco2_estimado") else 100.0,
                    "tco2e_verified": float(payload.get("tco2_verificado")) if payload.get("tco2_verificado") else 100.0,
                    "status": payload.get("estado_ejecucion") or "planificado"
                }
                new_inter = Intervention(**inter_attrs)
                db.add(new_inter)
                db.flush()
                
                staging_rec.status = "imported"
                staging_rec.imported_entity_id = new_inter.id
                imported_id = new_inter.id

            # 4. Case: MRV Observations Ingestion (04_mrv_avances_indicadores.xlsx)
            elif req.filename == "04_mrv_avances_indicadores.xlsx":
                entered_inter_id = payload.get("intervencion_id")
                target_inter = db.query(Intervention).filter(Intervention.id == entered_inter_id).first() if entered_inter_id else None
                if not target_inter:
                    target_inter = db.query(Intervention).first()
                    
                entered_ind_id = payload.get("indicador_id")
                target_ind = db.query(MRVIndicator).filter(MRVIndicator.id == entered_ind_id).first() if entered_ind_id else None
                if not target_ind:
                    target_ind = db.query(MRVIndicator).first()
                    
                mrv_attrs = {
                    "intervention_id": target_inter.id if target_inter else 1,
                    "indicator_id": target_ind.id if target_ind else 1,
                    "estimated_value": float(payload.get("valor_estimado")) if payload.get("valor_estimado") else 0.0,
                    "verified_value": float(payload.get("valor_verificado")) if payload.get("valor_verificado") else 0.0,
                    "verification_status": payload.get("estado_verificacion") or "estimated",
                    "notes": payload.get("observaciones") or "Ingresado directamente."
                }
                new_mrv = MRVObservation(**mrv_attrs)
                db.add(new_mrv)
                db.flush()
                
                staging_rec.status = "imported"
                staging_rec.imported_entity_id = new_mrv.id
                imported_id = new_mrv.id
                
            # 5. Case: GIS Layers Ingestion (06_catalogo_fuentes_datos_capas.xlsx)
            elif req.filename == "06_catalogo_fuentes_datos_capas.xlsx":
                layer_attrs = {
                    "name": payload.get("nombre_capa") or "Nueva Capa GIS",
                    "category": payload.get("categoria_capa") or "territorial",
                    "description": payload.get("descripcion_capa") or "Capa ingresada.",
                    "source_url": payload.get("url_capa") or "",
                    "geometry_type": payload.get("tipo_geometria") or "polygon",
                    "is_official": str(payload.get("es_oficial")).lower() in ("yes", "true", "1"),
                    "is_active": str(payload.get("es_activa")).lower() in ("yes", "true", "1")
                }
                new_layer = Layer(**layer_attrs)
                db.add(new_layer)
                db.flush()
                
                staging_rec.status = "imported"
                staging_rec.imported_entity_id = new_layer.id
                imported_id = new_layer.id
                
            # Generic Fallback Mapper (for any other XLSX form fields)
            else:
                target_mapping = {
                    "03_intervenciones_utcuts_geometria.xlsx": ("intervention", Intervention),
                    "04_mrv_avances_indicadores.xlsx": ("mrv", MRVObservation),
                    "06_catalogo_fuentes_datos_capas.xlsx": ("layer", Layer)
                }
                
                mapping_details = target_mapping.get(req.filename)
                if mapping_details:
                    model_name, model_class = mapping_details
                    model_attrs = {}
                    columns = [c.name for c in model_class.__table__.columns]
                    
                    for k, v in payload.items():
                        if k in columns:
                            if v is not None and str(v).strip() != "":
                                model_attrs[k] = v
                                
                    new_record = model_class(**model_attrs)
                    db.add(new_record)
                    db.flush()
                    
                    staging_rec.status = "imported"
                    staging_rec.imported_entity_id = new_record.id
                    imported_id = new_record.id
                    
        except Exception as db_err:
            db.rollback()
            staging_rec.status = "failed"
            staging_rec.validation_errors = json.dumps([{
                "field": "db_transaction",
                "label": "Transacción Base de Datos",
                "error": f"Error persistiendo registro en tablas reales: {str(db_err)}"
            }])
            status = "failed"
            validation_errors = [{"field": "db_transaction", "error": str(db_err)}]

    db.commit()
    
    return {
        "status": staging_rec.status,
        "staging_id": staging_rec.id,
        "imported_entity_id": imported_id,
        "validation_errors": validation_errors,
        "form_id": form_meta["form_id"],
        "form_title": form_meta["form_title"]
    }
