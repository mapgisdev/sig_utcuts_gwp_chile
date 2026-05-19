"""Seed real geospatial data — loads Regional.json and comunas.json into local SQLite db."""
import json
import os
import random
import sys

# Add backend root to python path to allow importing app
backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(backend_dir)

from sqlalchemy import text
from app.db.session import SessionLocal

# Import all models so they register with Base.metadata to prevent foreign key errors
from app.models import user, territory, mechanism, project, investment  # noqa
from app.models import intervention, mrv, prioritization, data_quality  # noqa
from app.models import layer, evidence, audit  # noqa

from app.models.territory import Territory
from app.models.prioritization import PrioritizationScore

def run_real_geo_seeding():
    db = SessionLocal()
    try:
        print("Starting real geospatial seeding...")
        
        # 1. Clear old data
        print("Clearing old data from territories and dependencies...")
        db.execute(text("DELETE FROM project_territories"))
        db.execute(text("DELETE FROM prioritization_scores"))
        db.execute(text("DELETE FROM territories"))
        db.commit()
        
        # 2. Add Country: Chile
        chile = Territory(
            code="CL",
            name="Chile",
            type="country",
            is_sample=False,
            area_ha=75610000
        )
        db.add(chile)
        db.flush()
        chile_id = chile.id
        print("  Added Country: Chile")
        
        # 3. Load Regional.json
        # Paths are relative to the execution context (backend/ directory)
        reg_path = os.path.join(backend_dir, "..", "insumos", "datos_geo", "Regional.json")
        print(f"Loading regions from {reg_path}...")
        with open(reg_path, "r", encoding="utf-8") as f:
            reg_data = json.load(f)
            
        region_map = {}  # Maps codregion -> Territory object
        
        for feat in reg_data["features"]:
            props = feat["properties"]
            geom = feat["geometry"]
            
            # Map attributes
            codregion = str(props["codregion"])
            name = props["Region"]
            
            # Area
            st_area = props.get("st_area_sh", 0)
            area_km = props.get("area_km", 0)
            area_ha = (st_area / 10000.0) if st_area else (area_km * 100.0)
            
            reg_obj = Territory(
                code=f"CL-{codregion.zfill(2)}",
                name=name,
                type="region",
                parent_id=chile_id,
                geom_geojson=json.dumps(geom),
                area_ha=area_ha,
                is_sample=False
            )
            db.add(reg_obj)
            db.flush()
            region_map[codregion] = reg_obj
            print(f"  Loaded Region: {name} (CL-{codregion.zfill(2)})")
            
        # 4. Load comunas.json
        com_path = os.path.join(backend_dir, "..", "insumos", "datos_geo", "comunas.json")
        print(f"Loading communes from {com_path}...")
        with open(com_path, "r", encoding="utf-8") as f:
            com_data = json.load(f)
            
        random.seed(42)
        commune_count = 0
        
        for feat in com_data["features"]:
            props = feat["properties"]
            geom = feat["geometry"]
            
            # Map attributes
            cod_comuna = str(props["cod_comuna"])
            name = props["Comuna"]
            codregion = str(props["codregion"])
            
            # Get parent region
            parent = region_map.get(codregion)
            parent_id = parent.id if parent else None
            
            # Area
            st_area = props.get("st_area_sh", 0)
            area_ha = (st_area / 10000.0) if st_area else 1000.0
            
            com_obj = Territory(
                code=cod_comuna.zfill(5),
                name=name,
                type="commune",
                parent_id=parent_id,
                geom_geojson=json.dumps(geom),
                area_ha=area_ha,
                is_sample=False
            )
            db.add(com_obj)
            db.flush()
            commune_count += 1
            
            # Generate PrioritizationScore
            # Let's add some regional flavor to the scores
            sf = round(random.uniform(30, 95), 1)
            # Higher climate risk in North (Coquimbo, Arica, Tarapacá, Antofagasta, Atacama -> codregion 15, 1, 2, 3, 4)
            if codregion in ["15", "1", "2", "3", "4"]:
                sc = round(random.uniform(75, 98), 1)
            else:
                sc = round(random.uniform(20, 80), 1)
                
            sd = round(random.uniform(15, 85), 1)
            sg = round(random.uniform(25, 90), 1)
            sb = round(random.uniform(10, 80), 1)
            ss = round(random.uniform(20, 85), 1)
            so = round(random.uniform(30, 90), 1)
            sm = round(random.uniform(10, 70), 1)
            
            # Total score calculation
            total = round(0.20*sf + 0.15*sc + 0.15*sd + 0.15*sg + 0.10*sb + 0.10*ss + 0.10*so + 0.05*sm, 1)
            
            if total >= 75: pc = "muy_alta"
            elif total >= 60: pc = "alta"
            elif total >= 45: pc = "media"
            elif total >= 25: pc = "baja"
            else: pc = "muy_baja"
            
            score_obj = PrioritizationScore(
                territory_id=com_obj.id,
                scenario_name="default",
                score_total=total,
                score_forest_restoration=sf,
                score_climate_risk=sc,
                score_degradation_loss=sd,
                score_financial_gap=sg,
                score_biodiversity=sb,
                score_social_vulnerability=ss,
                score_operational_feasibility=so,
                score_mechanism_alignment=sm,
                priority_class=pc,
                is_sample=False
            )
            db.add(score_obj)
            
        db.commit()
        print(f"\n[OK] Successfully loaded {len(region_map)} regions and {commune_count} communes with prioritization scores!")
        
    except Exception as e:
        db.rollback()
        print(f"\n[ERROR] Seeding failed: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    run_real_geo_seeding()
