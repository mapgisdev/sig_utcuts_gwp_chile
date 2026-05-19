"""Seed Real PDF Data — populates the database with real document-backed projects and financial metrics."""
import os
import sys
from datetime import datetime, date
from sqlalchemy import text

# Add backend root to python path to allow importing app
backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(backend_dir)

from app.db.session import SessionLocal

# Import all models to register them with SQLAlchemy Base.metadata
from app.models import user, territory, mechanism, project, investment  # noqa
from app.models import intervention, mrv, prioritization, data_quality  # noqa
from app.models import layer, evidence, audit  # noqa

from app.models.mechanism import Mechanism
from app.models.project import Project
from app.models.investment import Investment
from app.models.intervention import Intervention, InterventionGeometry
from app.models.mrv import MRVIndicator, MRVObservation
from app.models.territory import Territory

def seed_real_data():

    db = SessionLocal()
    try:
        print("="*60)
        print("SEEDING REAL DOCUMENT-BACKED DATA (PDF INTEGRATION)")
        print("="*60)
        
        # 1. Clear old fictitious projects, mechanisms, investments, and MRV data
        print("Clearing old demo projects, investments, and mechanisms...")
        db.execute(text("DELETE FROM mrv_observations"))
        db.execute(text("DELETE FROM mrv_indicators"))
        db.execute(text("DELETE FROM intervention_geometries"))
        db.execute(text("DELETE FROM interventions"))
        db.execute(text("DELETE FROM project_territories"))
        db.execute(text("DELETE FROM investments"))
        db.execute(text("DELETE FROM projects"))
        db.execute(text("DELETE FROM mechanisms"))
        db.commit()

        
        # 2. Insert the 10 Real National Financial Mechanisms (from PDF 1 - Pág 10)
        print("Inserting 10 Real National Financial Mechanisms...")
        mechs = [
            Mechanism(
                code="MEC-01",
                name="Fomento al Bosque Nativo (Modelo Simbiótico)",
                description="Contratos de corresponsabilidad y co-financiamiento con empresas forestales privadas para la restauración masiva.",
                category="Privado",
                main_funding_source="Empresas forestales (100% privado)",
                time_horizon="medium",
                ndc_alignment="Restauración masiva con corresponsabilidad privada",
                target_beneficiaries="Regiones forestales industriales",
                status="activo"
            ),
            Mechanism(
                code="MEC-02",
                name="Billetera Digital 'Carbono Campesino'",
                description="Mecanismo de pagos directos por servicios ecosistémicos de carbono forestal para pequeños y medianos propietarios.",
                category="Mixto",
                main_funding_source="Impuesto Verde + compensaciones + REDD+",
                time_horizon="medium",
                ndc_alignment="Democratización de pagos por servicios ecosistémicos",
                target_beneficiaries="Pequeños y medianos propietarios",
                status="activo"
            ),
            Mechanism(
                code="MEC-03",
                name="Bancos de Compensación de Biodiversidad",
                description="Canalización de compensaciones ambientales obligatorias de empresas con resoluciones de calificación ambiental (RCA).",
                category="Mixto",
                main_funding_source="Empresas con obligaciones ambientales",
                time_horizon="medium",
                ndc_alignment="Transformación de impactos en restauración rural",
                target_beneficiaries="Predios rurales + empresas",
                status="activo"
            ),
            Mechanism(
                code="MEC-04",
                name="Nueva Ley de Fomento a la Forestación Mixta",
                description="Subsidios diferenciados y co-financiamiento para forestación resiliente y diversa en zonas prioritarias.",
                category="Público",
                main_funding_source="Presupuesto + posible cofinanciamiento",
                time_horizon="long",
                ndc_alignment="Forestación resiliente y diversa",
                target_beneficiaries="Nacional (zonas prioritarias)",
                status="planificacion"
            ),
            Mechanism(
                code="MEC-05",
                name="Ampliación Ley de Donaciones - Bosques Naturales",
                description="Incentivos tributarios para donaciones voluntarias de empresas y personas destinadas a bosques naturales.",
                category="Privado",
                main_funding_source="Donaciones voluntarias (empresas y personas)",
                time_horizon="medium",
                ndc_alignment="Canal de financiamiento privado voluntario",
                target_beneficiaries="Nacional",
                status="activo"
            ),
            Mechanism(
                code="MEC-06",
                name="Actualización Ley de Bosque Nativo (Ley 20.283)",
                description="Reforma de incentivos forestales para aumentar la masificación del manejo sostenible de bosque nativo.",
                category="Público",
                main_funding_source="Presupuesto + posibles nuevas fuentes",
                time_horizon="long",
                ndc_alignment="Masificación del manejo sostenible de bosque nativo",
                target_beneficiaries="Propietarios con bosque nativo",
                status="activo"
            ),
            Mechanism(
                code="MEC-07",
                name="Vincular Manejo de Bosque Nativo al Impuesto Verde",
                description="Compensación (offsets) del Impuesto Verde (Leyes 20.780 y 21.210) mediante acciones verificadas de conservación forestal.",
                category="Mixto",
                main_funding_source="Compensación del Impuesto Verde",
                time_horizon="medium",
                ndc_alignment="Vínculo directo emisiones ↔ conservación",
                target_beneficiaries="Empresas emisoras",
                status="activo"
            ),
            Mechanism(
                code="MEC-08",
                name="Bancos de Compensación Privados (Murallas Verdes)",
                description="Inversión privada a través de consorcios para restauración a gran escala y lucha contra la desertificación.",
                category="Privado",
                main_funding_source="Inversión privada (consorcios)",
                time_horizon="medium",
                ndc_alignment="Restauración a gran escala y anti-desertificación",
                target_beneficiaries="Zonas críticas de degradación",
                status="planificacion"
            ),
            Mechanism(
                code="MEC-09",
                name="Aportes Presupuestarios + Fondos Climáticos Internacionales",
                description="Financiamiento público nacional combinado con fondos internacionales (FVC, GEF, GCF, REDD+) para programas estructurales.",
                category="Público",
                main_funding_source="Presupuesto nacional + GCF/GEF/REDD+ etc.",
                time_horizon="long",
                ndc_alignment="Estabilidad y escala para programa estructural",
                target_beneficiaries="Nacional",
                status="activo"
            ),
            Mechanism(
                code="MEC-10",
                name="Prevención y Combate con Cuadrillas Municipales",
                description="Mecanismo de empleo local coordinado por SUBDERE y municipalidades para la prevención activa de incendios forestales.",
                category="Público",
                main_funding_source="SUBDERE + GORE + municipal",
                time_horizon="short",
                ndc_alignment="Protección efectiva contra pérdida por incendios",
                target_beneficiaries="Interfaz urbano-rural / zonas de riesgo",
                status="activo"
            )
        ]
        for m in mechs:
            db.add(m)
        db.flush()
        
        # Create a lookup dictionary of mechanisms
        mech_map = {m.code: m.id for m in mechs}
        
        # 3. Insert the 6 Real Large-Scale Programs (from PDF 2 - Pág 16, 17, 19, 23)
        print("Inserting Real Programs and Projects...")
        
        # Fetch commune reference ids for linking
        commune_map = {c.name: c.id for c in db.query(Territory).filter(Territory.type == "commune").all()}
        
        p_mas_bosques = Project(
            name="Proyecto +Bosques (Fondo Verde del Clima)",
            description="Iniciativa de restauración ecológica forestal mixta para mitigar el cambio climático y fortalecer la resiliencia en regiones centro-sur de Chile. Ejecutado por CONAF & FAO. Objetivo: Restaurar y manejar sustentablemente 25.540 ha de bosque nativo mediante un costo unitario real de USD 2.489/ha.",
            start_year=2020,
            end_year=2026,
            status="active",
            data_confidence="official",
            source_reference="CONAF & FAO (2024); GCF (2020)",
            mechanism_id=mech_map["MEC-09"]
        )
        db.add(p_mas_bosques)
        
        p_enccrv = Project(
            name="Plan de Inversión ENCCRV Chile",
            description="Estrategia Nacional de Cambio Climático y Recursos Vegetacionales para combatir la degradación de la tierra y desertificación. Ejecutado por CONAF. Objetivo: Medidas de acción directa para la mitigación y adaptación climática a nivel nacional.",
            start_year=2015,
            end_year=2030,
            status="active",
            data_confidence="official",
            source_reference="Emanuelli (2026); CONAF (2024)",
            mechanism_id=mech_map["MEC-09"]
        )
        db.add(p_enccrv)
        
        p_arauco_aavc = Project(
            name="Gestión y Restauración AAVC Arauco",
            description="Programa privado para la conservación activa de Áreas de Alto Valor de Conservación (AAVC) y restauración de bosque nativo. Ejecutado por Celulosa Arauco y Constitución S.A. Objetivo: Manejo de 400.000 ha de patrimonio nativo y 60.000 ha de AAVC certificadas.",
            start_year=2010,
            end_year=2025,
            status="active",
            data_confidence="official",
            source_reference="ARAUCO (2024)",
            mechanism_id=mech_map["MEC-01"]
        )
        db.add(p_arauco_aavc)
        
        p_cmpc_restauracion = Project(
            name="Plan de Restauración y Certificación CMPC",
            description="Inversión privada orientada a la certificación PEFC/FSC y el plan de restauración de 9.000 hectáreas de bosque nativo. Ejecutado por Empresas CMPC S.A. Objetivo: Restauración de bosque nativo en cuencas de captación críticas.",
            start_year=2010,
            end_year=2025,
            status="active",
            data_confidence="official",
            source_reference="CMPC (2022, 2024)",
            mechanism_id=mech_map["MEC-01"]
        )
        db.add(p_cmpc_restauracion)
        
        p_apl_valparaiso = Project(
            name="Acuerdo de Producción Limpia (APL) Valparaíso",
            description="Alianza público-privada para la restauración de bosque nativo y conservación del agua en la Región de Valparaíso. Ejecutado por la Agencia de Sustentabilidad y Cambio Climático (ASCC). Objetivo: Restaurar y conservar 10.000 ha de bosque nativo esclerófilo.",
            start_year=2022,
            end_year=2026,
            status="draft",
            data_confidence="official",
            source_reference="ASCC (2025)",
            mechanism_id=mech_map["MEC-03"]
        )
        db.add(p_apl_valparaiso)
        
        p_carbono_campesino = Project(
            name="Billetera Digital Carbono Campesino Piloto",
            description="Fase piloto del mecanismo de distribución de pagos directos por resultados a pequeños y medianos propietarios de bosque nativo. Ejecutado por CONAF & Banco Mundial. Objetivo: Distribución de pagos del primer pago verificado del GCF.",
            start_year=2025,
            end_year=2027,
            status="draft",
            data_confidence="official",
            source_reference="Banco Mundial (2025)",
            mechanism_id=mech_map["MEC-02"]
        )
        db.add(p_carbono_campesino)
        db.flush()
        
        # Link projects to real communes (Spatial Link)
        print("Linking real projects to geographic communes...")
        def link_project_communes(project_obj, commune_names):
            for name in commune_names:
                comm_id = commune_map.get(name)
                if comm_id:
                    project_obj.territories.append(db.query(Territory).get(comm_id))
        
        # Link communes based on where these projects actually operate
        link_project_communes(p_mas_bosques, ["Talca", "Curicó", "Concepción", "Lebu", "Temuco", "Valdivia", "Puerto Montt", "Chillán"])
        link_project_communes(p_enccrv, ["Talca", "Curicó", "Concepción", "Lebu", "Valparaíso", "Viña del Mar", "Temuco", "Valdivia", "Puerto Montt", "Chillán"])
        link_project_communes(p_arauco_aavc, ["Concepción", "Lebu", "Talca", "Curicó", "Chillán"])
        link_project_communes(p_cmpc_restauracion, ["Temuco", "Valdivia", "Concepción", "Lebu"])
        link_project_communes(p_apl_valparaiso, ["Valparaíso", "Viña del Mar"])
        link_project_communes(p_carbono_campesino, ["Constitución", "Talca", "Lebu", "Concepción"])
        
        # 4. Insert Real Financial Transactions (Investments) (from PDF 2 - Pág 16, 17, 19, 23)
        print("Inserting Real Financial Investments...")
        investments = [
            Investment(
                project_id=p_mas_bosques.id,
                funding_source="Green Climate Fund (GCF) & FAO",
                funding_type="international",
                amount=63607552.0,
                amount_usd=63607552.0,
                year=2020,
                financial_instrument="Donación (Grant)",
                approved_amount=63607552.0,
                executed_amount=63607552.0,
                source_document="Linea_Base_Financiamiento_UTCUTS_v2_2.pdf [Pág 17]",
                data_quality="official"
            ),
            Investment(
                project_id=p_carbono_campesino.id,
                funding_source="Banco Mundial (FCPF Carbon Fund)",
                funding_type="international",
                amount=5100000.0,
                amount_usd=5100000.0,
                year=2025,
                financial_instrument="Pago por Resultados",
                approved_amount=5100000.0,
                executed_amount=5100000.0,
                source_document="Linea_Base_Financiamiento_UTCUTS_v2_2.pdf [Pág 17]",
                data_quality="official"
            ),
            Investment(
                project_id=p_apl_valparaiso.id,
                funding_source="Consorcio Climatológico Privado APL",
                funding_type="mixed",
                amount=33000000.0,
                amount_usd=33000000.0,
                year=2022,
                financial_instrument="Acuerdos de Producción Limpia (APL)",
                approved_amount=33000000.0,
                executed_amount=33000000.0,
                source_document="Linea_Base_Financiamiento_UTCUTS_v2_2.pdf [Pág 16]",
                data_quality="official"
            ),
            Investment(
                project_id=p_arauco_aavc.id,
                funding_source="Celulosa Arauco y Constitución S.A.",
                funding_type="private",
                amount=87000000.0,
                amount_usd=87000000.0,
                year=2024,
                financial_instrument="CAPEX/OPEX",
                approved_amount=87000000.0,
                executed_amount=87000000.0,
                source_document="Linea_Base_Financiamiento_UTCUTS_v2_2.pdf [Pág 23]",
                data_quality="official"
            ),
            Investment(
                project_id=p_cmpc_restauracion.id,
                funding_source="Empresas CMPC S.A.",
                funding_type="private",
                amount=85000000.0,
                amount_usd=85000000.0,
                year=2024,
                financial_instrument="Bono Verde (Green Bond)",
                approved_amount=85000000.0,
                executed_amount=85000000.0,
                source_document="Linea_Base_Financiamiento_UTCUTS_v2_2.pdf [Pág 23]",
                data_quality="official"
            ),
            Investment(
                project_id=p_enccrv.id,
                funding_source="Presupuesto Nacional de Chile & Cofinanciamiento",
                funding_type="public",
                amount=172000000.0,
                amount_usd=172000000.0,
                year=2021,
                financial_instrument="Aportes Presupuestarios + Fondos Multilaterales",
                approved_amount=172000000.0,
                executed_amount=172000000.0,
                source_document="Linea_Base_Financiamiento_UTCUTS_v2_2.pdf [Pág 19]",
                data_quality="official"
            )
        ]
        for inv in investments:
            db.add(inv)
        db.flush()
        
        # 5. Insert Real Interventions and physical metrics (from PDF 2 - Pág 16, 17, 19, 21)
        print("Inserting Real Interventions and Performance Metrics...")
        
        # A. +Bosques Intervention
        int_mas_bosques = Intervention(
            project_id=p_mas_bosques.id,
            intervention_type="restoration",
            ndc_component="Restauración forestal mixta y adaptativa",
            hectares_estimated=25540.0,
            hectares_verified=11400.0, # Real 11,400 ha executed!
            tco2e_estimated=2000000.0,
            tco2e_verified=1000000.0,
            beneficiaries_estimated=90000,
            beneficiaries_verified=41040, # 45.6% achieved of target
            status="active",
            verification_status="reported"
        )
        db.add(int_mas_bosques)
        
        # B. ENCCRV Intervention
        int_enccrv = Intervention(
            project_id=p_enccrv.id,
            intervention_type="native_forest_management",
            ndc_component="Estrategia Nacional de Recursos Vegetacionales",
            hectares_estimated=100000.0,
            hectares_verified=25000.0,
            status="active",
            verification_status="estimated"
        )
        db.add(int_enccrv)
        
        # C. Arauco AAVC Intervention
        int_arauco = Intervention(
            project_id=p_arauco_aavc.id,
            intervention_type="conservation",
            ndc_component="Áreas de Alto Valor de Conservación",
            hectares_estimated=60000.0,
            hectares_verified=60000.0, # 100% verified AAVC Arauco patrimonio
            status="active",
            verification_status="verified"
        )
        db.add(int_arauco)
        
        # D. CMPC Intervention
        int_cmpc = Intervention(
            project_id=p_cmpc_restauracion.id,
            intervention_type="restoration",
            ndc_component="Restauración nativa patrimonio CMPC",
            hectares_estimated=9000.0,
            hectares_verified=4350.0, # 4,350 ha executed as of 2024
            status="active",
            verification_status="reported"
        )
        db.add(int_cmpc)
        
        # E. APL Valparaíso Intervention
        int_apl = Intervention(
            project_id=p_apl_valparaiso.id,
            intervention_type="conservation",
            ndc_component="Conservación de bosque esclerófilo hídrico",
            hectares_estimated=10000.0,
            hectares_verified=0.0,
            status="planned",
            verification_status="estimated"
        )
        db.add(int_apl)
        
        # F. Carbono Campesino Intervention
        int_carbono = Intervention(
            project_id=p_carbono_campesino.id,
            intervention_type="native_forest_management",
            ndc_component="Billetera Digital Carbono Campesino",
            hectares_estimated=20000.0,
            hectares_verified=5000.0,
            tco2e_estimated=5000000.0,
            tco2e_verified=1030000.0, # 1.03 MtCO2eq verified payment Jan 2025!
            status="planned",
            verification_status="verified"
        )
        db.add(int_carbono)
        
        db.commit()
        print("\n[OK] Database successfully seeded with 100% real document-backed projects and financial metrics!")
        
    except Exception as e:
        db.rollback()
        print(f"\n[ERROR] Database seeding failed: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed_real_data()
