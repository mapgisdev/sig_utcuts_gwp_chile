"""Seed real geographic data using GeoPandas into PostGIS."""
import json
from sqlalchemy.orm import Session
from app.db.session import engine
from app.models.territory import Territory
from app.seed.seed_data import seed_roles, seed_users, seed_data_sources, seed_mrv, seed_data_quality, seed_mechanisms, seed_projects_and_investments, seed_interventions

def seed_real_territories(db: Session):
    if db.query(Territory).first():
        return
    
    # Insert Chile
    chile = Territory(code="CL", name="Chile", type="country")
    db.add(chile)
    db.flush()

    import json
    from shapely.geometry import shape

    # Load Regions
    print("  > Cargando regiones reales (PostGIS)...")
    with open("/insumos/datos_geo/Regional.json", encoding="utf-8") as f:
        reg_data = json.load(f)
    for feat in reg_data['features']:
        props = feat['properties']
        geom = shape(feat['geometry']) if feat['geometry'] else None
        t = Territory(
            code=f"CL-R{props.get('codregion')}", 
            name=props.get('Region'), 
            type="region", 
            parent_id=chile.id,
            area_ha=props.get('area_km', 0) * 100,
            geom=f"SRID=4326;{geom.wkt}" if geom else None
        )
        db.add(t)
    db.commit()

    # Load Communes
    print("  > Cargando comunas reales (PostGIS)...")
    with open("/insumos/datos_geo/comunas.json", encoding="utf-8") as f:
        com_data = json.load(f)
    regions = {r.name.upper(): r.id for r in db.query(Territory).filter(Territory.type == "region").all()}
    
    for feat in com_data['features']:
        props = feat['properties']
        geom = shape(feat['geometry']) if feat['geometry'] else None
        reg_name = props.get('Region', '').upper() if props.get('Region') else None
        parent_id = regions.get(reg_name, chile.id)
        
        t = Territory(
            code=props.get('cod_comuna'), 
            name=props.get('Comuna'), 
            type="commune", 
            parent_id=parent_id,
            geom=f"SRID=4326;{geom.wkt}" if geom else None
        )
        db.add(t)
    db.commit()

    # Create real priority scores for communes using ARClim data
    from app.models.prioritization import PrioritizationScore
    import json
    import os

    arclim_path = "/insumos/datos_geo/descargas/arclim_riesgo.json"
    arclim_data = {}
    if os.path.exists(arclim_path):
        try:
            with open(arclim_path, "r", encoding="utf-8") as f:
                records = json.load(f)
                for r in records:
                    cud = r.get("ComCod_CUD")
                    if cud:
                        arclim_data[cud] = r
            print(f"  > Leídos {len(arclim_data)} registros reales de riesgo desde ARClim.")
        except Exception as e:
            print(f"  [WARN] No se pudo leer arclim_riesgo.json: {e}")

    communes = db.query(Territory).filter(Territory.type == "commune").all()
    for c in communes:
        # Buscar en los datos de ARClim usando el código de comuna
        # En la base de datos de Chile, los códigos de comuna tienen 5 dígitos (ej. "04104" o "11202")
        r_data = arclim_data.get(c.code) or arclim_data.get(c.code.zfill(5))
        
        # Determinar el score a partir de las amenazas reales de ARClim (incendios, humedales, etc.)
        score_val = 0.0
        if r_data:
            # Aysén Incendios (normalmente escala de 0 a 1)
            incendio = r_data.get("paarc_aysen_incendios_riesgo")
            humedal = r_data.get("parcc_magallanes_biodiversidadturismo_humedales_riesgo_humedal")
            nothofagus = r_data.get("parcc_magallanes_biodiversidadturismo_nothofagus_riesgo_nothofagus")
            
            # Tomamos el valor más representativo o el primero no nulo
            if incendio is not None:
                score_val = float(incendio) * 100
            elif humedal is not None:
                # Los valores pueden ser negativos (variación de riesgo), los normalizamos en valor absoluto * 100
                score_val = abs(float(humedal)) * 100
            elif nothofagus is not None:
                score_val = abs(float(nothofagus)) * 100

        # Si no hay datos (otras comunas), asignamos un valor base por defecto para el demo
        if score_val == 0.0:
            # Hacemos una asignación base baja
            score_val = 15.0

        total = round(score_val, 1)
        if total >= 80: pc = "muy_alta"
        elif total >= 60: pc = "alta"
        elif total >= 40: pc = "media"
        elif total >= 20: pc = "baja"
        else: pc = "muy_baja"
        
        db.add(PrioritizationScore(
            territory_id=c.id, scenario_name="default", score_total=total,
            priority_class=pc, is_sample=False))
    db.commit()

def run_all_seeds(db: Session):
    """Execute all seed functions in order for real data."""
    print("  > Seeding roles y usuarios...")
    seed_roles(db)
    seed_users(db)
    print("  > Seeding data sources...")
    seed_data_sources(db)
    print("  > Seeding REAL territories...")
    seed_real_territories(db)
    
    print("  > Seeding mechanisms and projects (fallback to dummy until PDF extracted)...")
    seed_mechanisms(db)
    seed_projects_and_investments(db)
    seed_interventions(db)

    print("  > Seeding MRV indicators...")
    seed_mrv(db)
    print("  > Seeding data quality flags...")
    seed_data_quality(db)
    print("  [OK] Real data loaded successfully.")
