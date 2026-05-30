"""Tests for all 9 XLSForms dynamic ingestion and database mapping."""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.session import SessionLocal
from app.models.intervention import Intervention, InterventionGeometry
from app.models.mrv import MRVObservation
from app.models.evidence import EvidenceFile
from app.models.layer import DataSource, Layer
from app.models.data_quality import DataQualityFlag
from app.models.kobo import KoboStagingRecord

client = TestClient(app)

def test_xlsform_ingestion_interventions():
    """Test 03_intervenciones_utcuts_geometria.xlsx ingestion."""
    payload = {
        "start": "2026-05-26",
        "end": "2026-05-26",
        "today": "2026-05-26",
        "codigo_intervencion": "INT-TEST-03",
        "codigo_proyecto": "PROJ-NATIVE-TEST-99",
        "tipo_intervencion": "restauracion_ecosistemas",
        "componente_ndc": "i1_manejo_bosque_nativo",
        "fecha_intervencion": "2026-05-26",
        "estado_intervencion": "en_ejecucion",
        "regiones": "r07_maule",
        "tipo_geometria": "geopoint",
        "geom_punto": "-35.43 71.62 0 0",
        "superficie_ha": "25.5",
        "estado_verificacion": "revisado_tecnico",
        "fuente_geometria": "GPS Garmin",
        "nivel_confianza": "alto"
    }
    
    r = client.post("/api/v1/kobo/staging/simulate-sync", json={
        "filename": "03_intervenciones_utcuts_geometria.xlsx",
        "payload": payload
    })
    assert r.status_code == 200
    res = r.json()
    assert res["status"] == "imported"
    assert res["imported_entity_id"] is not None
    
    db = SessionLocal()
    try:
        inter = db.query(Intervention).get(res["imported_entity_id"])
        assert inter is not None
        assert inter.intervention_type == "restauracion_ecosistemas"
        assert inter.hectares_estimated == 25.5
        assert inter.hectares_verified == 25.5
        
        # Verify geometry record was created
        geom = db.query(InterventionGeometry).filter(InterventionGeometry.intervention_id == inter.id).first()
        assert geom is not None
        assert geom.geometry_type == "point"
        assert "Point" in geom.geom_geojson
        
        # Cleanup
        db.delete(geom)
        db.delete(inter)
        staging = db.get(KoboStagingRecord, res["staging_id"])
        if staging:
            db.delete(staging)
        db.commit()
    finally:
        db.close()

def test_xlsform_ingestion_mrv_avances():
    """Test 04_mrv_avances_indicadores.xlsx ingestion."""
    payload = {
        "start": "2026-05-26",
        "end": "2026-05-26",
        "today": "2026-05-26",
        "codigo_mrv": "MRV-TEST-04",
        "codigo_proyecto": "PROJ-NATIVE-TEST-99",
        "codigo_intervencion": "1",
        "periodo_inicio": "2026-01-01",
        "periodo_fin": "2026-05-26",
        "tipo_avance": "reportado",
        "monto_periodo": "125000",
        "moneda": "USD",
        "avance_financiero_pct": "75",
        "ha_restauradas": "15.8",
        "ha_forestadas": "0",
        "tco2e_verificadas_periodo": "340.5",
        "estado_verificacion": "verificado_externo",
        "observaciones": "Avances primer semestre verificado"
    }
    
    r = client.post("/api/v1/kobo/staging/simulate-sync", json={
        "filename": "04_mrv_avances_indicadores.xlsx",
        "payload": payload
    })
    assert r.status_code == 200
    res = r.json()
    assert res["status"] == "imported"
    
    db = SessionLocal()
    try:
        # Multiple observations should be created
        obs_list = db.query(MRVObservation).filter(MRVObservation.notes.like("%Avances primer semestre%")).all()
        assert len(obs_list) > 0
        
        # Verify specific indicators were created
        restauradas_created = False
        monto_created = False
        
        for obs in obs_list:
            if obs.indicator.code == "FIS-02":
                assert obs.verified_value == 15.8
                restauradas_created = True
            elif obs.indicator.code == "FIN-02":
                assert obs.verified_value == 125000
                monto_created = True
                
        assert restauradas_created
        assert monto_created
        
        # Cleanup
        for obs in obs_list:
            db.delete(obs)
        staging = db.get(KoboStagingRecord, res["staging_id"])
        if staging:
            db.delete(staging)
        db.commit()
    finally:
        db.close()

def test_xlsform_ingestion_evidencias():
    """Test 05_evidencias_validacion.xlsx ingestion."""
    payload = {
        "start": "2026-05-26",
        "end": "2026-05-26",
        "today": "2026-05-26",
        "codigo_evidencia": "EVID-TEST-05",
        "codigo_proyecto": "PROJ-NATIVE-TEST-99",
        "tipo_evidencia": "informe",
        "url_documento": "http://example.com/informe.pdf",
        "descripcion_evidencia": "Informe de validación ambiental",
        "fecha_evidencia": "2026-05-26",
        "estado_validacion": "revisado_tecnico"
    }
    
    r = client.post("/api/v1/kobo/staging/simulate-sync", json={
        "filename": "05_evidencias_validacion.xlsx",
        "payload": payload
    })
    assert r.status_code == 200
    res = r.json()
    assert res["status"] == "imported"
    
    db = SessionLocal()
    try:
        ev = db.query(EvidenceFile).get(res["imported_entity_id"])
        assert ev is not None
        assert ev.file_type == "informe"
        assert ev.file_path == "http://example.com/informe.pdf"
        assert ev.entity_type == "project"
        
        # Cleanup
        db.delete(ev)
        staging = db.get(KoboStagingRecord, res["staging_id"])
        if staging:
            db.delete(staging)
        db.commit()
    finally:
        db.close()

def test_xlsform_ingestion_capas():
    """Test 06_catalogo_fuentes_datos_capas.xlsx Ingestion."""
    payload = {
        "start": "2026-05-26",
        "end": "2026-05-26",
        "today": "2026-05-26",
        "codigo_fuente": "SRC-TEST-06",
        "nombre_fuente": "Capa Test Ingesta",
        "institucion_responsable": "MMA",
        "tipo_fuente": "geojson",
        "url_acceso": "http://example.com/capa.json",
        "cobertura_territorial": "comuna",
        "uso_en_sig": "Visualización de áreas prioritarias",
        "estado_integracion": "integrada_bd",
        "nivel_confianza": "alto"
    }
    
    r = client.post("/api/v1/kobo/staging/simulate-sync", json={
        "filename": "06_catalogo_fuentes_datos_capas.xlsx",
        "payload": payload
    })
    assert r.status_code == 200
    res = r.json()
    assert res["status"] == "imported"
    
    db = SessionLocal()
    try:
        layer = db.query(Layer).get(res["imported_entity_id"])
        assert layer is not None
        assert layer.name == "Capa Test Ingesta"
        assert layer.source_url == "http://example.com/capa.json"
        assert layer.is_active is True
        
        # Verify linked DataSource was created
        ds = layer.data_source
        assert ds is not None
        assert ds.name == "Capa Test Ingesta"
        assert ds.institution == "MMA"
        
        # Cleanup
        db.delete(layer)
        db.delete(ds)
        staging = db.get(KoboStagingRecord, res["staging_id"])
        if staging:
            db.delete(staging)
        db.commit()
    finally:
        db.close()

def test_xlsform_ingestion_brechas():
    """Test 08_brechas_calidad_datos.xlsx ingestion."""
    payload = {
        "start": "2026-05-26",
        "end": "2026-05-26",
        "today": "2026-05-26",
        "codigo_brecha": "BRECHA-TEST-08",
        "modulo_afectado": "inversiones",
        "tipo_brecha": "sin_monto",
        "descripcion_brecha": "Inversión registrada sin monto definido",
        "gravedad": "alta",
        "impacto_en_sistema": "Métricas de inversión distorsionadas",
        "accion_recomendada": "Revisar resolución exenta",
        "fecha_identificacion": "2026-05-26",
        "estado_brecha": "abierta"
    }
    
    r = client.post("/api/v1/kobo/staging/simulate-sync", json={
        "filename": "08_brechas_calidad_datos.xlsx",
        "payload": payload
    })
    assert r.status_code == 200
    res = r.json()
    assert res["status"] == "imported"
    
    db = SessionLocal()
    try:
        flag = db.query(DataQualityFlag).get(res["imported_entity_id"])
        assert flag is not None
        assert flag.entity_type == "investment"
        assert flag.flag_type == "missing_amount"
        assert flag.severity == "error"
        assert flag.resolved is False
        
        # Cleanup
        db.delete(flag)
        staging = db.get(KoboStagingRecord, res["staging_id"])
        if staging:
            db.delete(staging)
        db.commit()
    finally:
        db.close()

def test_xlsform_ingestion_actores():
    """Test 07_actores_organizaciones.xlsx validation and staging."""
    payload = {
        "start": "2026-05-26",
        "end": "2026-05-26",
        "today": "2026-05-26",
        "codigo_actor": "ACT-TEST-07",
        "nombre_actor": "Organización de Prueba",
        "tipo_actor": "publico",
        "roles_sistema": "financiador",
        "nivel_confianza": "alto",
        "estado_registro": "validado"
    }
    
    r = client.post("/api/v1/kobo/staging/simulate-sync", json={
        "filename": "07_actores_organizaciones.xlsx",
        "payload": payload
    })
    assert r.status_code == 200
    res = r.json()
    assert res["status"] == "validated"
    
    db = SessionLocal()
    try:
        staging = db.get(KoboStagingRecord, res["staging_id"])
        assert staging is not None
        assert staging.status == "validated"
        db.delete(staging)
        db.commit()
    finally:
        db.close()

def test_xlsform_ingestion_variables():
    """Test 09_variables_priorizacion.xlsx validation and staging."""
    payload = {
        "start": "2026-05-26",
        "end": "2026-05-26",
        "today": "2026-05-26",
        "codigo_variable": "VAR-TEST-09",
        "nombre_variable": "Variable de Prueba",
        "dimension": "forestal",
        "descripcion_variable": "Descripción de variable de prueba",
        "fuente_datos": "CONAF",
        "unidad_medida": "Porcentaje",
        "escala_calculo": "comuna",
        "sentido_priorizacion": "mayor_es_mejor",
        "metodo_normalizacion": "minmax",
        "peso_default": 0.15,
        "variable_activa": "yes",
        "nivel_confianza": "alto"
    }
    
    r = client.post("/api/v1/kobo/staging/simulate-sync", json={
        "filename": "09_variables_priorizacion.xlsx",
        "payload": payload
    })
    assert r.status_code == 200
    res = r.json()
    assert res["status"] == "validated"
    
    db = SessionLocal()
    try:
        staging = db.get(KoboStagingRecord, res["staging_id"])
        assert staging is not None
        assert staging.status == "validated"
        db.delete(staging)
        db.commit()
    finally:
        db.close()

