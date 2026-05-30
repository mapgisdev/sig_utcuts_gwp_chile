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
from app.models.intervention import Intervention, InterventionGeometry
from app.models.mrv import MRVObservation, MRVIndicator
from app.models.layer import Layer, DataSource
from app.models.evidence import EvidenceFile
from app.models.data_quality import DataQualityFlag
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
        try:            # 1. SPECIAL CASE: Project + Investment Joint Ingestion (from 02_registro_inversiones_proyectos.xlsx)
            if req.filename == "02_registro_inversiones_proyectos.xlsx":
                # Handle start and end years dynamically from dates
                start_yr = 2026
                f_start = payload.get("fecha_inicio") or payload.get("fecha_registro")
                if f_start:
                    try:
                        start_yr = int(str(f_start)[:4])
                    except:
                        pass
                elif payload.get("anio_inicio"):
                    try:
                        start_yr = int(payload.get("anio_inicio"))
                    except:
                        pass

                end_yr = 2030
                f_end = payload.get("fecha_fin")
                if f_end:
                    try:
                        end_yr = int(str(f_end)[:4])
                    except:
                        pass
                elif payload.get("anio_fin"):
                    try:
                        end_yr = int(payload.get("anio_fin"))
                    except:
                        pass

                # Status mapping
                st_proj = "draft"
                ep = payload.get("estado_proyecto") or payload.get("estado_registro")
                if ep in ("activo", "aprobado", "en_ejecucion"):
                    st_proj = "active"
                elif ep == "finalizado":
                    st_proj = "completed"
                elif ep in ("suspendido", "cancelado", "rechazado"):
                    st_proj = "cancelled"

                # Confidence / Quality
                conf = payload.get("nivel_confianza") or payload.get("calidad_dato")
                if conf in ("alto", "high", "official"):
                    conf = "high"
                elif conf in ("medio", "medium"):
                    conf = "medium"
                elif conf in ("bajo", "low"):
                    conf = "low"
                else:
                    conf = "demo"

                proj_attrs = {
                    "name": payload.get("nombre_proyecto") or "Nuevo Proyecto XLSForm",
                    "description": payload.get("descripcion_proyecto") or "Ingresado directamente desde el formulario nativo.",
                    "start_year": start_yr,
                    "end_year": end_yr,
                    "source_reference": payload.get("codigo_proyecto") or payload.get("referencia_fuente") or "Formulario Operativo",
                    "data_confidence": conf,
                    "geographic_precision": payload.get("precision_geografica") or "comuna"
                }
                
                # Fetch mechanism by code or default
                m_code = payload.get("codigo_mecanismo")
                target_mech = None
                if m_code:
                    target_mech = db.query(Mechanism).filter(Mechanism.code == m_code).first()
                if not target_mech:
                    target_mech = db.query(Mechanism).first()
                proj_attrs["mechanism_id"] = target_mech.id if target_mech else 1
                
                new_project = Project(**proj_attrs)
                db.add(new_project)
                db.flush()

                # Link territories
                # Comuna
                c_code = payload.get("codigo_comuna") or payload.get("comuna_codigo")
                if c_code:
                    commune = db.query(Territory).filter(Territory.code == str(c_code), Territory.type == "commune").first()
                    if commune:
                        new_project.territories.append(commune)
                
                # Regions
                regs = payload.get("regiones")
                if regs:
                    for r_code in str(regs).split():
                        digits = "".join(filter(str.isdigit, r_code))
                        region = db.query(Territory).filter(Territory.code == digits, Territory.type == "region").first()
                        if region:
                            new_project.territories.append(region)
                
                # Create linked Investment
                f_source = payload.get("fuente_financiamiento") or "Inversión Directa Operativa"
                f_type = "mixed"
                if f_source:
                    if "publico" in f_source or "municipal" in f_source:
                        f_type = "public"
                    elif "privado" in f_source:
                        f_type = "private"
                    elif "internacional" in f_source:
                        f_type = "international"
                if payload.get("tipo_financiamiento"):
                    f_type = payload.get("tipo_financiamiento")
                
                # Montos
                m_aprobado = float(payload.get("monto_aprobado")) if payload.get("monto_aprobado") else None
                m_comprometido = float(payload.get("monto_comprometido")) if payload.get("monto_comprometido") else None
                m_ejecutado = float(payload.get("monto_ejecutado")) if payload.get("monto_ejecutado") else None
                
                amount_val = float(payload.get("monto_inversion")) if payload.get("monto_inversion") else (m_aprobado or m_comprometido or m_ejecutado or 100000.0)
                amount_usd_val = float(payload.get("monto_usd")) if payload.get("monto_usd") else amount_val

                inv_attrs = {
                    "project_id": new_project.id,
                    "funding_source": payload.get("actor_financiador") or f_source,
                    "funding_type": f_type,
                    "amount": amount_val,
                    "amount_usd": amount_usd_val,
                    "year": int(payload.get("anio_inversion")) if payload.get("anio_inversion") else start_yr,
                    "financial_instrument": payload.get("instrumento_financiero") or "Aporte Directo",
                    "approved_amount": m_aprobado or amount_val,
                    "executed_amount": m_ejecutado or amount_val,
                    "committed_amount": m_comprometido or amount_val,
                    "source_document": payload.get("documento_fuente") or payload.get("fuente_documental") or "Direct Submission",
                    "data_quality": conf
                }
                new_investment = Investment(**inv_attrs)
                db.add(new_investment)
                db.flush()
                
                staging_rec.status = "imported"
                staging_rec.imported_entity_id = new_project.id
                imported_id = new_project.id
                
            # 2. Case: Mechanisms Ingestion (01_catalogo_mecanismos.xlsx)
            elif req.filename == "01_catalogo_mecanismos.xlsx":
                th = payload.get("horizonte_temporal")
                if th == "corto": th = "short"
                elif th == "mediano": th = "medium"
                elif th == "largo": th = "long"
                
                mat = payload.get("estado_madurez")
                if mat == "idea": mat = "concept"
                elif mat == "diseno": mat = "design"
                elif mat == "piloto": mat = "pilot"
                elif mat == "operacion": mat = "operational"
                elif mat == "escalamiento": mat = "scaling"
                
                st = "active"
                if payload.get("estado_registro") == "borrador":
                    st = "draft"
                
                mech_attrs = {
                    "code": payload.get("codigo_mecanismo") or f"MEC-{datetime.utcnow().timestamp()}",
                    "name": payload.get("nombre_mecanismo") or "Mecanismo Ingestado",
                    "category": payload.get("categoria_mecanismo") or "legal",
                    "description": payload.get("descripcion_mecanismo") or "Creado nativamente.",
                    "main_funding_source": payload.get("fuente_principal") or "Presupuesto",
                    "time_horizon": th or payload.get("horizonte_temporal"),
                    "maturity_level": mat or payload.get("estado_madurez"),
                    "ndc_alignment": payload.get("alineacion_ndc") or "Mitigación",
                    "target_beneficiaries": payload.get("beneficiarios_objetivo") or "Público",
                    "enabling_conditions": payload.get("condiciones_habilitantes"),
                    "intervention_types": payload.get("tipos_intervencion"),
                    "status": st
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
                p_code = payload.get("codigo_proyecto")
                target_proj = None
                if p_code:
                    target_proj = db.query(Project).filter(Project.source_reference == p_code).first()
                if not target_proj:
                    entered_proj_id = payload.get("proyecto_id")
                    target_proj = db.query(Project).filter(Project.id == entered_proj_id).first() if entered_proj_id else None
                if not target_proj:
                    target_proj = db.query(Project).first()
                
                st = payload.get("estado_intervencion") or payload.get("estado_ejecucion")
                if st == "en_ejecucion": st = "ongoing"
                elif st == "finalizado": st = "completed"
                elif not st: st = "planned"
                
                sup = float(payload.get("superficie_ha") or payload.get("hectareas_estimadas") or 10.0)
                hectares_est = sup
                hectares_ver = sup if payload.get("estado_verificacion") in ("revisado_tecnico", "verificado_externo", "verified") else 0.0
                
                tco2_est = float(payload.get("tco2_estimado") or payload.get("tco2e_estimated") or 100.0)
                tco2_ver = float(payload.get("tco2_verificado") or payload.get("tco2e_verified") or 0.0)
                    
                inter_attrs = {
                    "project_id": target_proj.id if target_proj else 1,
                    "intervention_type": payload.get("tipo_intervencion") or "restauracion",
                    "ndc_component": payload.get("componente_ndc") or "Mitigación",
                    "hectares_estimated": hectares_est,
                    "hectares_verified": hectares_ver,
                    "tco2e_estimated": tco2_est,
                    "tco2e_verified": tco2_ver,
                    "status": st
                }
                new_inter = Intervention(**inter_attrs)
                db.add(new_inter)
                db.flush()
                
                # Check for spatial geometry fields
                new_geom = None
                geom_type = payload.get("tipo_geometria")
                if geom_type and geom_type != "sin_geometria":
                    new_geom = InterventionGeometry(
                        intervention_id=new_inter.id,
                        geometry_type="point" if geom_type == "geopoint" else "polygon",
                        source=payload.get("fuente_geometria") or "Formulario XLSForm",
                        validated=payload.get("estado_verificacion") in ("revisado_tecnico", "verificado_externo")
                    )
                    
                    if payload.get("geom_punto"):
                        try:
                            # XLSForm point is "lat lng alt acc" -> GeoJSON uses [lng, lat]
                            parts = payload.get("geom_punto").split()
                            if len(parts) >= 2:
                                lat = float(parts[0])
                                lng = float(parts[1])
                                new_geom.geom_geojson = json.dumps({
                                    "type": "Point",
                                    "coordinates": [lng, lat]
                                })
                        except:
                            pass
                    elif payload.get("geom_poligono"):
                        try:
                            # space-separated coordinates
                            pts = payload.get("geom_poligono").split()
                            coords = []
                            for i in range(0, len(pts), 4):
                                if i+1 < len(pts):
                                    lat = float(pts[i])
                                    lng = float(pts[i+1])
                                    coords.append([lng, lat])
                            if coords:
                                if coords[0] != coords[-1]:
                                    coords.append(coords[0])
                                new_geom.geom_geojson = json.dumps({
                                    "type": "Polygon",
                                    "coordinates": [coords]
                                })
                        except:
                            pass
                    
                    if new_geom and new_geom.geom_geojson:
                        db.add(new_geom)
                        db.flush()
                
                staging_rec.status = "imported"
                staging_rec.imported_entity_id = new_inter.id
                imported_id = new_inter.id

            # 4. Case: MRV Observations Ingestion (04_mrv_avances_indicadores.xlsx)
            elif req.filename == "04_mrv_avances_indicadores.xlsx":
                intv_code = payload.get("codigo_intervencion")
                target_inter = None
                if intv_code:
                    try:
                        target_inter = db.query(Intervention).filter(Intervention.id == int(intv_code)).first()
                    except:
                        pass
                if not target_inter:
                    target_inter = db.query(Intervention).first()
                    
                obs_date = datetime.utcnow().date()
                if payload.get("periodo_fin"):
                    try:
                        obs_date = datetime.strptime(payload.get("periodo_fin"), "%Y-%m-%d").date()
                    except:
                        pass
                
                # Multiple observations mapping
                indicator_mappings = {
                    "monto_periodo": "FIN-02",
                    "avance_financiero_pct": "FIN-03",
                    "ha_manejo_bosque_nativo": "FIS-01",
                    "ha_restauradas": "FIS-02",
                    "ha_forestadas": "FIS-03",
                    "ha_conservadas": "BIO-01",
                    "tco2e_verificadas_periodo": "CLI-01",
                    "tco2e_estimadas_periodo": "CLI-02",
                    "beneficiarios_total": "SOC-01",
                }
                
                obs_status = payload.get("estado_verificacion")
                if obs_status in ("verificado_externo", "revisado_tecnico", "verified"):
                    obs_status = "verified"
                else:
                    obs_status = "estimated"
                
                first_obs = None
                for col_name, ind_code in indicator_mappings.items():
                    val = payload.get(col_name)
                    if val is not None and str(val).strip() != "":
                        try:
                            num_val = float(val)
                            if num_val > 0:
                                ind = db.query(MRVIndicator).filter(MRVIndicator.code == ind_code).first()
                                if ind:
                                    # Create observation
                                    new_obs = MRVObservation(
                                        intervention_id=target_inter.id if target_inter else 1,
                                        indicator_id=ind.id,
                                        estimated_value=num_val if "estimadas" in col_name else None,
                                        verified_value=num_val if "estimadas" not in col_name else None,
                                        observation_date=obs_date,
                                        verification_status=obs_status,
                                        notes=payload.get("observaciones") or f"Ingresado desde XLSForm {col_name}."
                                    )
                                    db.add(new_obs)
                                    db.flush()
                                    if not first_obs:
                                        first_obs = new_obs
                        except:
                            pass
                
                # Single observation fallback (for backwards-compatibility in tests)
                if not first_obs:
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
                    first_obs = MRVObservation(**mrv_attrs)
                    db.add(first_obs)
                    db.flush()
                
                staging_rec.status = "imported"
                staging_rec.imported_entity_id = first_obs.id
                imported_id = first_obs.id
                
            # 5. Case: Evidence Files Ingestion (05_evidencias_validacion.xlsx)
            elif req.filename == "05_evidencias_validacion.xlsx":
                ent_type = "project"
                ent_id = 1
                
                mrv_code = payload.get("codigo_mrv")
                intv_code = payload.get("codigo_intervencion")
                proj_code = payload.get("codigo_proyecto")
                
                if mrv_code:
                    ent_type = "mrv_observation"
                    try:
                        obs = db.query(MRVObservation).filter(MRVObservation.id == int(mrv_code)).first()
                        if obs:
                            ent_id = obs.id
                    except:
                        pass
                elif intv_code:
                    ent_type = "intervention"
                    try:
                        intv = db.query(Intervention).filter(Intervention.id == int(intv_code)).first()
                        if intv:
                            ent_id = intv.id
                    except:
                        pass
                elif proj_code:
                    ent_type = "project"
                    proj = db.query(Project).filter(Project.source_reference == proj_code).first()
                    if proj:
                        ent_id = proj.id
                        
                file_name_val = payload.get("foto_evidencia") or payload.get("url_documento") or "evidencia_xlsform.jpg"
                
                new_evidence = EvidenceFile(
                    filename=file_name_val,
                    original_name=file_name_val,
                    file_type=payload.get("tipo_evidencia") or "image",
                    file_path=payload.get("url_documento") or "/evidence/uploads/" + file_name_val,
                    entity_type=ent_type,
                    entity_id=ent_id,
                    is_sample=False
                )
                db.add(new_evidence)
                db.flush()
                
                if ent_type == "mrv_observation" and ent_id != 1:
                    obs = db.query(MRVObservation).get(ent_id)
                    if obs:
                        obs.evidence_file_id = new_evidence.id
                        
                staging_rec.status = "imported"
                staging_rec.imported_entity_id = new_evidence.id
                imported_id = new_evidence.id

            # 6. Case: GIS Layers Ingestion (06_catalogo_fuentes_datos_capas.xlsx)
            elif req.filename == "06_catalogo_fuentes_datos_capas.xlsx":
                new_ds = DataSource(
                    name=payload.get("nombre_fuente") or "Nueva Fuente de Datos",
                    institution=payload.get("institucion_responsable") or "CONAF",
                    category=payload.get("cobertura_territorial") or "regional",
                    url=payload.get("url_acceso"),
                    update_frequency=payload.get("periodicidad_actualizacion"),
                    license=payload.get("licencia_uso"),
                    spatial_resolution=payload.get("escala_resolucion"),
                    temporal_resolution=payload.get("cobertura_temporal"),
                    geometry_type=payload.get("tipo_fuente") or "vector",
                    integration_status=payload.get("estado_integracion") or "planned",
                    notes=payload.get("observaciones") or payload.get("uso_en_sig"),
                    is_sample=False
                )
                db.add(new_ds)
                db.flush()
                
                new_layer = Layer(
                    name=payload.get("nombre_fuente") or payload.get("nombre_capa") or "Nueva Capa GIS",
                    description=payload.get("uso_en_sig") or payload.get("descripcion_capa") or payload.get("observaciones"),
                    category=payload.get("cobertura_territorial") or payload.get("categoria_capa") or "territorial",
                    data_source_id=new_ds.id,
                    source_url=payload.get("url_acceso") or payload.get("url_capa"),
                    geometry_type=payload.get("tipo_fuente") or payload.get("tipo_geometria") or "polygon",
                    layer_type=payload.get("tipo_fuente") or payload.get("tipo_geometria") or "geojson",
                    is_official=payload.get("nivel_confianza") == "alto" or str(payload.get("es_oficial")).lower() in ("yes", "true", "1"),
                    is_active=payload.get("estado_integracion") in ("integrada_bd", "publicada_mapa") or str(payload.get("es_activa")).lower() in ("yes", "true", "1"),
                    is_sample=False
                )
                db.add(new_layer)
                db.flush()
                
                staging_rec.status = "imported"
                staging_rec.imported_entity_id = new_layer.id
                imported_id = new_layer.id

            # 7. Case: Data Quality Ingestion (08_brechas_calidad_datos.xlsx)
            elif req.filename == "08_brechas_calidad_datos.xlsx":
                mod = payload.get("modulo_afectado")
                e_type = "project"
                if mod == "inversiones": e_type = "investment"
                elif mod == "intervenciones": e_type = "intervention"
                
                ft = payload.get("tipo_brecha") or "other"
                if ft == "sin_geometria": ft = "missing_geometry"
                elif ft == "sin_monto": ft = "missing_amount"
                elif ft == "sin_fuente": ft = "missing_source"
                
                sev = payload.get("gravedad") or "warning"
                if sev == "baja": sev = "info"
                elif sev == "media": sev = "warning"
                elif sev == "alta": sev = "error"
                elif sev == "critica": sev = "critical"
                
                new_flag = DataQualityFlag(
                    entity_type=e_type,
                    entity_id=1,
                    flag_type=ft,
                    severity=sev,
                    description=payload.get("descripcion_brecha") or "Identificada vía XLSForm",
                    resolved=payload.get("estado_brecha") == "resuelta",
                    is_sample=False
                )
                db.add(new_flag)
                db.flush()
                
                staging_rec.status = "imported"
                staging_rec.imported_entity_id = new_flag.id
                imported_id = new_flag.id

            # Generic fallback mapping
            else:
                staging_rec.status = "validated"
                    
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
