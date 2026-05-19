"""Integration Test — verifies direct native database promotion and joint multi-model insertions."""
import os
import sys

backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(backend_dir)

from fastapi.testclient import TestClient
from app.main import app

def test_kobo_native_ingestion():
    with TestClient(app) as client:
        print("="*75)
        print("RUNNING DIRECT NATIVE DATABASE PROMOTION INTEGRATION TESTS")
        print("="*75)
        
        # 1. Test forms discovery list
        res = client.get("/api/v1/kobo/forms")
        print(f"1. GET /api/v1/kobo/forms - Status: {res.status_code}")
        forms = res.json()
        print(f"   Detected {len(forms)} XLSForms in folder.")
        
        # 2. Test Mechanism Native Promotion (01_catalogo_mecanismos.xlsx)
        print("\n2. TESTING MECHANISM DIRECT NATIVE INGESTION (01_catalogo_mecanismos.xlsx)")
        mech_payload = {
            "start": "2026-05-18",
            "end": "2026-05-18",
            "today": "2026-05-18",
            "username": "tester",
            "deviceid": "dev-123",
            "codigo_mecanismo": "MEC-NATIVE-TEST-99",
            "nombre_mecanismo": "Mecanismo Ingestado Nativo",
            "categoria_mecanismo": "legal",
            "descripcion_mecanismo": "Prueba de ingesta nativa directa sin vinculacion API.",
            "fuente_principal": "Fondo Verde Regional",
            "instrumento_principal": "Subsidio",
            "horizonte_temporal": "medium",
            "estado_madurez": "operational",
            "alineacion_ndc": "Mitigacion Forestal",
            "tipos_intervencion": "restauracion",
            "beneficiarios_objetivo": "Comunidades",
            "actores_clave": "CONAF",
            "condiciones_habilitantes": "Reglamento",
            "indicadores_clave": "ha",
            "precision_geografica": "alta",
            "regiones_potenciales": "Biobío",
            "criterios_elegibilidad_territorial": "Priorizacion",
            "nivel_confianza": "alta",
            "estado_registro": "activo",
            "observaciones": "Ninguna"
        }
        res = client.post("/api/v1/kobo/staging/simulate-sync", json={
            "filename": "01_catalogo_mecanismos.xlsx",
            "payload": mech_payload
        })
        print(f"   Status Code: {res.status_code}")
        res_data = res.json()
        print(f"   Ingestion Status: '{res_data['status']}'")
        print(f"   Staging Record ID: {res_data['staging_id']}")
        print(f"   Imported Production Mechanism ID: {res_data['imported_entity_id']}")
        print(f"   Validation Errors: {res_data['validation_errors']}")
        
        # 3. Test Project + Investment Joint Native Promotion (02_registro_inversiones_proyectos.xlsx)
        print("\n3. TESTING JOINT PROJECT + INVESTMENT NATIVE INGESTION (02_registro_inversiones_proyectos.xlsx)")
        project_payload = {
            "start": "2026-05-18",
            "end": "2026-05-18",
            "today": "2026-05-18",
            "username": "tester",
            "deviceid": "dev-123",
            "codigo_mecanismo": "MEC-1",  # required by project XLSForm as a parent code
            "codigo_proyecto": "PROJ-NATIVE-TEST-99",
            "nombre_proyecto": "Proyecto Reforestación Nativa Test",
            "descripcion_proyecto": "Prueba de mapeo e insercion relacional de dos modelos en base de datos.",
            "anio_inicio": "2026",
            "anio_fin": "2031",
            "estado_proyecto": "activo",
            "actor_financiador": "GWP",
            "moneda": "USD",
            "precision_geografica": "comuna",
            "regiones": "Maule",
            "tipos_intervencion": "restauracion",
            "alineacion_ndc": "mitigacion",
            "referencia_fuente": "Licitación MMA 2026",
            "nivel_confianza": "high",
            
            # Investment properties (split natively)
            "fuente_financiamiento": "Fondo Multilateral Araucanía",
            "tipo_financiamiento": "mixed",
            "monto_inversion": "2500000.0",
            "monto_usd": "2500000.0",
            "anio_inversion": "2026",
            "instrumento_financiero": "Subsidio Estatal y Privado",
            "monto_aprobado": "2500000.0",
            "monto_ejecutado": "500000.0",
            "monto_comprometido": "2000000.0",
            "documento_fuente": "Res. Exenta N° 82",
            "calidad_dato": "official",
            "estado_registro": "activo"
        }
        res = client.post("/api/v1/kobo/staging/simulate-sync", json={
            "filename": "02_registro_inversiones_proyectos.xlsx",
            "payload": project_payload
        })
        print(f"   Status Code: {res.status_code}")
        res_data_proj = res.json()
        print(f"   Ingestion Status: '{res_data_proj['status']}'")
        print(f"   Staging Record ID: {res_data_proj['staging_id']}")
        print(f"   Imported Production Project ID: {res_data_proj['imported_entity_id']}")
        print(f"   Validation Errors: {res_data_proj['validation_errors']}")
        
        # 4. Verify promotions inside direct SQLite Tables
        from app.db.session import SessionLocal
        from app.models.mechanism import Mechanism
        from app.models.project import Project
        from app.models.investment import Investment
        from app.models.kobo import KoboStagingRecord
        
        db = SessionLocal()
        inv = None
        try:
            # Check mechanism promotion
            mech = db.query(Mechanism).filter(Mechanism.code == "MEC-NATIVE-TEST-99").first()
            if mech:
                print(f"\n[SUCCESS] Verified in Mechanism Table: ID={mech.id}, Name='{mech.name}'")
            else:
                print("\n[ERROR] Mechanism not found in database.")
                
            # Check project promotion
            proj = db.query(Project).filter(Project.name == "Proyecto Reforestación Nativa Test").first()
            if proj:
                print(f"[SUCCESS] Verified in Project Table: ID={proj.id}, Name='{proj.name}'")
                
                # Check associated investment promotion linked by project_id
                inv = db.query(Investment).filter(Investment.project_id == proj.id).first()
                if inv:
                    print(f"[SUCCESS] Verified Relational Joint Investment Table: ID={inv.id}, Approved Amount={inv.approved_amount}, Funding Type='{inv.funding_type}'")
                else:
                    print("[ERROR] Relational Investment not found in database for project.")
            else:
                print("[ERROR] Project not found in database.")
                
            # Clean up test rows
            if mech:
                db.delete(mech)
            if proj:
                # delete investment first to maintain foreign key constraint
                if inv:
                    db.delete(inv)
                db.delete(proj)
            
            # Delete staging logs
            staging_mech = db.get(KoboStagingRecord, res_data['staging_id'])
            staging_proj = db.get(KoboStagingRecord, res_data_proj['staging_id'])
            if staging_mech:
                db.delete(staging_mech)
            if staging_proj:
                db.delete(staging_proj)
                
            db.commit()
            print("   Cleaned up test records from database successfully.")
        except Exception as cleanup_err:
            db.rollback()
            print(f"   [CLEANUP ERROR] {cleanup_err}")
        finally:
            db.close()
        print("="*75)

if __name__ == "__main__":
    test_kobo_native_ingestion()
