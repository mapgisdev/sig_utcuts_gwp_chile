"""Seed data loader — synthetic demo data for SIG-UTCUTS Chile."""
import json
from datetime import datetime, date
from sqlalchemy.orm import Session
from app.models.user import User, Role
from app.models.territory import Territory
from app.models.mechanism import Mechanism
from app.models.project import Project
from app.models.investment import Investment
from app.models.intervention import Intervention
from app.models.mrv import MRVIndicator, MRVObservation
from app.models.data_quality import DataQualityFlag
from app.models.prioritization import PrioritizationScore
from app.models.layer import DataSource, Layer
from app.core.security import get_password_hash


def _bbox_to_geojson(x1, y1, x2, y2):
    """Convert bounding box to GeoJSON polygon string."""
    geom = {
        "type": "Polygon",
        "coordinates": [[[x1, y1], [x2, y1], [x2, y2], [x1, y2], [x1, y1]]]
    }
    return json.dumps(geom)


def seed_roles(db: Session):
    roles = ["public_viewer", "institutional_viewer", "analyst", "editor", "validator", "admin"]
    for r in roles:
        if not db.query(Role).filter(Role.name == r).first():
            db.add(Role(name=r, description=f"Rol {r}"))
    db.commit()


def seed_users(db: Session):
    admin_role = db.query(Role).filter(Role.name == "admin").first()
    editor_role = db.query(Role).filter(Role.name == "editor").first()
    viewer_role = db.query(Role).filter(Role.name == "public_viewer").first()
    if db.query(User).filter(User.username == "admin").first():
        return
    users = [
        User(email="admin@sigutcuts.demo", username="admin",
             hashed_password=get_password_hash("admin123"),
             full_name="Administrador Demo", institution="CONAF", is_sample=True,
             roles=[admin_role] if admin_role else []),
        User(email="editor@sigutcuts.demo", username="editor",
             hashed_password=get_password_hash("editor123"),
             full_name="Editor Demo", institution="MMA", is_sample=True,
             roles=[editor_role] if editor_role else []),
        User(email="viewer@sigutcuts.demo", username="viewer",
             hashed_password=get_password_hash("viewer123"),
             full_name="Visor Demo", institution="Público", is_sample=True,
             roles=[viewer_role] if viewer_role else []),
    ]
    db.add_all(users)
    db.commit()


def seed_territories(db: Session):
    if db.query(Territory).first():
        return
    # Country
    chile = Territory(code="CL", name="Chile", type="country", is_sample=True, area_ha=75610000)
    db.add(chile)
    db.flush()

    # Regions with simplified bounding-box polygons (EPSG:4326)
    regions_data = [
        ("CL-CO", "Coquimbo", -71.5, -29.0, -70.0, -32.2, 4058000),
        ("CL-VS", "Valparaíso", -71.8, -32.0, -70.0, -33.5, 1639630),
        ("CL-ML", "Maule", -72.5, -34.5, -70.3, -36.4, 3036000),
        ("CL-BI", "Biobío", -73.5, -36.4, -71.0, -38.0, 3706900),
    ]
    region_objs = []
    for code, name, x1, y1, x2, y2, area in regions_data:
        geojson = _bbox_to_geojson(x1, y1, x2, y2)
        r = Territory(code=code, name=name, type="region", parent_id=chile.id,
                      geom_geojson=geojson, area_ha=area, is_sample=True)
        db.add(r)
        db.flush()
        region_objs.append(r)

    # 2 communes per region
    communes = [
        ("04101", "La Serena", 0, -71.3, -29.9, -70.5, -30.3, 189000),
        ("04102", "Coquimbo", 0, -71.4, -30.0, -70.8, -30.5, 150000),
        ("05101", "Valparaíso", 1, -71.7, -33.0, -71.4, -33.1, 30000),
        ("05109", "Viña del Mar", 1, -71.6, -33.0, -71.4, -33.1, 17800),
        ("07101", "Talca", 2, -71.8, -35.3, -71.4, -35.6, 23200),
        ("07301", "Curicó", 2, -71.4, -34.9, -71.0, -35.2, 73200),
        ("08101", "Concepción", 3, -73.1, -36.7, -72.9, -36.9, 22100),
        ("08201", "Los Ángeles", 3, -72.6, -37.3, -72.0, -37.7, 180000),
    ]
    for code, name, ri, x1, y1, x2, y2, area in communes:
        geojson = _bbox_to_geojson(x1, y1, x2, y2)
        db.add(Territory(code=code, name=name, type="commune",
                         parent_id=region_objs[ri].id,
                         geom_geojson=geojson, area_ha=area, is_sample=True))
    db.commit()


def seed_mechanisms(db: Session):
    if db.query(Mechanism).first():
        return
    mechs = [
        ("MEC-01", "Actualización Ley de Bosque Nativo", "legal", "Presupuesto público", "design", "medium",
         "Manejo sostenible, conservación", "Pequeños y medianos propietarios forestales", "native_forest_management"),
        ("MEC-02", "Nueva Ley de Fomento a la Forestación Mixta", "legal", "Presupuesto público", "concept", "long",
         "Forestación, captura de carbono", "Propietarios de terrenos sin bosque", "afforestation"),
        ("MEC-03", "Ampliación Ley de Donaciones hacia Bosques Naturales", "fiscal", "Privado", "design", "medium",
         "Conservación, restauración", "ONG, comunidades", "conservation"),
        ("MEC-04", "Vincular Manejo de BN al Impuesto Verde", "fiscal", "Mixto", "concept", "long",
         "Reducción de emisiones", "Empresas emisoras", "native_forest_management"),
        ("MEC-05", "Bancos de Compensación de Biodiversidad", "market", "Privado", "pilot", "medium",
         "Biodiversidad, restauración", "Empresas con obligaciones de compensación", "conservation"),
        ("MEC-06", "Bancos de Compensación Privados / Murallas Verdes", "market", "Privado", "concept", "long",
         "Restauración, prevención de incendios", "Sector privado", "restoration"),
        ("MEC-07", "Fomento al Bosque Nativo / Modelo Simbiótico", "subsidy", "Público", "operational", "short",
         "Manejo de bosque nativo", "Pequeños propietarios", "native_forest_management"),
        ("MEC-08", "Billetera Digital de Carbono Campesino", "market", "Mixto", "concept", "long",
         "Carbono, inclusión social", "Campesinos, pequeños propietarios", "restoration"),
        ("MEC-09", "Cuadrillas Municipales de Prevención de Incendios", "public", "Público", "pilot", "short",
         "Prevención de incendios", "Municipios, comunidades rurales", "fire_prevention"),
        ("MEC-10", "Aportes Presupuestarios + Fondos Climáticos Internacionales", "international", "Internacional", "operational", "medium",
         "NDC, restauración, conservación", "Gobierno, instituciones", "restoration"),
    ]
    for code, name, cat, src, mat, th, ndc, ben, it in mechs:
        db.add(Mechanism(code=code, name=name, category=cat, main_funding_source=src,
                         maturity_level=mat, time_horizon=th, ndc_alignment=ndc,
                         target_beneficiaries=ben, intervention_types=it,
                         description=f"Mecanismo demo: {name}", is_sample=True))
    db.commit()


def seed_projects_and_investments(db: Session):
    if db.query(Project).first():
        return
    mechs = db.query(Mechanism).all()
    territories = db.query(Territory).filter(Territory.type == "commune").all()
    projects_data = [
        ("Restauración cuenca Elqui", 0, 2023, 2027, "regional", [0, 1]),
        ("Forestación Valparaíso", 1, 2024, 2028, "communal", [2, 3]),
        ("Conservación bosque nativo Maule", 2, 2022, 2026, "communal", [4, 5]),
        ("Prevención incendios Biobío", 8, 2024, 2025, "regional", [6, 7]),
        ("Carbono campesino piloto", 7, 2025, 2030, "national", [0, 1, 2, 3]),
        ("Compensación biodiversidad minera", 4, 2023, 2028, "communal", [4, 5]),
    ]
    for name, mi, sy, ey, gp, ti in projects_data:
        p = Project(mechanism_id=mechs[mi].id if mi < len(mechs) else None,
                    name=name, start_year=sy, end_year=ey,
                    status="active", geographic_precision=gp, data_confidence="demo",
                    source_reference="Dato sintético demo", is_sample=True)
        p.territories = [territories[i] for i in ti if i < len(territories)]
        db.add(p)
    db.flush()

    inv_data = [
        (1, "CONAF", "public", 5000000, 2023), (1, "GCF", "international", 3000000, 2024),
        (2, "FNDR", "public", 2000000, 2024), (2, "FAO", "international", 1500000, 2024),
        (3, "Ley Donaciones", "private", 800000, 2022), (3, "MMA", "public", 1200000, 2023),
        (4, "CONAF", "public", 600000, 2024), (4, "Municipios", "public", 400000, 2024),
        (5, "Banco Mundial", "international", 2500000, 2025),
        (5, "Privado", "private", 1000000, 2025),
        (6, "Empresa minera", "private", 3500000, 2023),
        (6, "GEF", "international", 1500000, 2024),
    ]
    for pi, src, ft, amt, yr in inv_data:
        db.add(Investment(project_id=pi, funding_source=src, funding_type=ft,
                          amount=amt, currency="USD", amount_usd=amt, year=yr,
                          data_quality="demo", is_sample=True))
    db.commit()


def seed_interventions(db: Session):
    if db.query(Intervention).first():
        return
    interventions = [
        (1, "restoration", 5000, 1200, 25000, 5000, 500, 120),
        (1, "native_forest_management", 3000, 800, 15000, 3000, 300, 80),
        (2, "afforestation", 4000, 0, 20000, 0, 200, 0),
        (3, "conservation", 8000, 2000, 40000, 10000, 150, 40),
        (4, "fire_prevention", 10000, 5000, 5000, 2500, 1000, 500),
        (5, "restoration", 2000, 0, 10000, 0, 100, 0),
        (6, "conservation", 6000, 1500, 30000, 7500, 50, 10),
        (6, "restoration", 3000, 500, 15000, 2500, 80, 20),
    ]
    for pi, it, he, hv, te, tv, be, bv in interventions:
        db.add(Intervention(project_id=pi, intervention_type=it,
                            hectares_estimated=he, hectares_verified=hv,
                            tco2e_estimated=te, tco2e_verified=tv,
                            beneficiaries_estimated=be, beneficiaries_verified=bv,
                            status="active",
                            verification_status="estimated" if hv == 0 else "reported",
                            is_sample=True))
    db.commit()


def seed_mrv(db: Session):
    if db.query(MRVIndicator).first():
        return
    indicators = [
        ("FIN-01", "Monto aprobado", "financial", "USD"),
        ("FIN-02", "Monto ejecutado", "financial", "USD"),
        ("FIN-03", "Porcentaje de ejecución", "financial", "%"),
        ("FIS-01", "Hectáreas bajo manejo", "physical", "ha"),
        ("FIS-02", "Hectáreas restauradas", "physical", "ha"),
        ("FIS-03", "Hectáreas forestadas", "physical", "ha"),
        ("CLI-01", "tCO2e capturadas", "climate", "tCO2e"),
        ("CLI-02", "Emisiones evitadas", "climate", "tCO2e"),
        ("SOC-01", "Beneficiarios directos", "social", "personas"),
        ("SOC-02", "Empleo generado", "social", "empleos"),
        ("BIO-01", "Superficie en áreas protegidas", "biodiversity", "ha"),
        ("BIO-02", "Ecosistemas cubiertos", "biodiversity", "unidades"),
        ("GOB-01", "Acuerdos firmados", "governance", "unidades"),
        ("CAL-01", "Registros completos", "data_quality", "%"),
        ("CAL-02", "Registros con geometría", "data_quality", "%"),
    ]
    for code, name, cat, unit in indicators:
        db.add(MRVIndicator(code=code, name=name, category=cat, unit=unit, is_sample=True))
    db.flush()

    inds = db.query(MRVIndicator).all()
    intrvs = db.query(Intervention).all()
    import random
    random.seed(42)
    for intv in intrvs[:5]:
        for ind in inds[:6]:
            est = round(random.uniform(100, 5000), 1)
            ver = round(est * random.uniform(0.2, 0.8), 1) if random.random() > 0.3 else None
            db.add(MRVObservation(
                intervention_id=intv.id, indicator_id=ind.id,
                estimated_value=est, verified_value=ver,
                observation_date=date(2024, 6, 15),
                verification_status="verified" if ver else "estimated",
                is_sample=True))
    db.commit()


def seed_prioritization(db: Session):
    if db.query(PrioritizationScore).first():
        return
    communes = db.query(Territory).filter(Territory.type == "commune").all()
    import random
    random.seed(42)
    for c in communes:
        sf = round(random.uniform(30, 95), 1)
        sc = round(random.uniform(20, 90), 1)
        sd = round(random.uniform(15, 85), 1)
        sg = round(random.uniform(25, 90), 1)
        sb = round(random.uniform(10, 80), 1)
        ss = round(random.uniform(20, 85), 1)
        so = round(random.uniform(30, 90), 1)
        sm = round(random.uniform(10, 70), 1)
        total = round(0.20*sf + 0.15*sc + 0.15*sd + 0.15*sg + 0.10*sb + 0.10*ss + 0.10*so + 0.05*sm, 1)
        if total >= 80: pc = "muy_alta"
        elif total >= 60: pc = "alta"
        elif total >= 40: pc = "media"
        elif total >= 20: pc = "baja"
        else: pc = "muy_baja"
        db.add(PrioritizationScore(
            territory_id=c.id, scenario_name="default", score_total=total,
            score_forest_restoration=sf, score_climate_risk=sc,
            score_degradation_loss=sd, score_financial_gap=sg,
            score_biodiversity=sb, score_social_vulnerability=ss,
            score_operational_feasibility=so, score_mechanism_alignment=sm,
            priority_class=pc, is_sample=True))
    db.commit()


def seed_data_quality(db: Session):
    if db.query(DataQualityFlag).first():
        return
    flags = [
        ("project", 3, "missing_geometry", "warning", "Proyecto sin geometría asociada"),
        ("investment", 5, "missing_source", "warning", "Inversión sin fuente documentada"),
        ("intervention", 3, "estimated_value", "info", "Valores solo estimados, sin verificación"),
        ("project", 5, "low_confidence", "warning", "Confianza baja en datos del proyecto"),
        ("investment", 9, "missing_year", "error", "Inversión sin año registrado"),
        ("intervention", 6, "missing_climate_indicator", "warning", "Sin indicador climático"),
        ("project", 2, "missing_geometry", "warning", "Proyecto sin geometría precisa"),
        ("investment", 11, "possible_duplicate", "info", "Posible duplicado con inversión 12"),
        ("intervention", 8, "missing_physical_indicator", "warning", "Sin indicador físico"),
        ("project", 4, "estimated_value", "info", "Hectáreas solo estimadas"),
    ]
    for et, eid, ft, sev, desc in flags:
        db.add(DataQualityFlag(entity_type=et, entity_id=eid, flag_type=ft,
                               severity=sev, description=desc, is_sample=True))
    db.commit()


def seed_data_sources(db: Session):
    if db.query(DataSource).first():
        return
    sources = [
        ("IDE Chile", "IDE Chile", "territorial", "https://www.ide.cl", "open"),
        ("CONAF SIT", "CONAF", "forest", "https://sit.conaf.cl", "open"),
        ("ARClim", "MMA / CR2", "climate", "https://arclim.mma.gob.cl", "open"),
        ("MapBiomas Chile", "MapBiomas", "land_cover", "https://chile.mapbiomas.org", "open"),
        ("SIMBIO", "MMA", "biodiversity", "https://simbio.mma.gob.cl", "restricted"),
    ]
    for name, inst, cat, url, acc in sources:
        db.add(DataSource(name=name, institution=inst, category=cat, url=url,
                          access_type=acc, integration_status="planned", is_sample=True))
    db.flush()
    ds_list = db.query(DataSource).all()
    layers = [
        ("Regiones de Chile", "territorial", 0, "polygon"),
        ("Comunas de Chile", "territorial", 0, "polygon"),
        ("Catastro Bosque Nativo", "forest", 1, "polygon"),
        ("Riesgo Climático Comunal", "climate", 2, "polygon"),
        ("Cobertura de Suelo", "land_cover", 3, "polygon"),
        ("Áreas Protegidas", "biodiversity", 4, "polygon"),
    ]
    for name, cat, dsi, gt in layers:
        db.add(Layer(name=name, category=cat,
                     data_source_id=ds_list[dsi].id if dsi < len(ds_list) else None,
                     geometry_type=gt, layer_type="geojson", is_sample=True))
    db.commit()


def run_all_seeds(db: Session):
    """Execute all seed functions in order."""
    print("  > Seeding roles...")
    seed_roles(db)
    print("  > Seeding users...")
    seed_users(db)
    print("  > Seeding data sources and layers...")
    seed_data_sources(db)
    print("  > Seeding territories...")
    seed_territories(db)
    print("  > Seeding mechanisms...")
    seed_mechanisms(db)
    print("  > Seeding projects and investments...")
    seed_projects_and_investments(db)
    print("  > Seeding interventions...")
    seed_interventions(db)
    print("  > Seeding MRV indicators and observations...")
    seed_mrv(db)
    print("  > Seeding prioritization scores...")
    seed_prioritization(db)
    print("  > Seeding data quality flags...")
    seed_data_quality(db)
    print("  [OK] All seed data loaded successfully.")
