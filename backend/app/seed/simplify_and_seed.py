"""Simplify and Seed — automatically optimizes and loads geographical boundaries."""
import json
import os
import random
import sys

# Add backend root to python path to allow importing app
backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(backend_dir)

from sqlalchemy import text
from app.db.session import SessionLocal

# Import all models to register them with SQLAlchemy Base.metadata
from app.models import user, territory, mechanism, project, investment  # noqa
from app.models import intervention, mrv, prioritization, data_quality  # noqa
from app.models import layer, evidence, audit  # noqa

from app.models.territory import Territory
from app.models.prioritization import PrioritizationScore

# --- PURE PYTHON RDP GEOMETRY SIMPLIFICATION ---

def distance_point_to_line(point, start, end):
    """Calculate perpendicular distance from a point to a line segment."""
    if start == end:
        return ((point[0] - start[0]) ** 2 + (point[1] - start[1]) ** 2) ** 0.5
    
    A = end[1] - start[1]
    B = start[0] - end[0]
    C = end[0] * start[1] - start[0] * end[1]
    
    num = abs(A * point[0] + B * point[1] + C)
    den = (A ** 2 + B ** 2) ** 0.5
    return num / den

def rdp(coords, epsilon):
    """Ramer-Douglas-Peucker algorithm to simplify a list of 2D coordinates."""
    if len(coords) < 3:
        return coords
        
    dmax = 0.0
    index = 0
    end = len(coords) - 1
    
    for i in range(1, end):
        d = distance_point_to_line(coords[i], coords[0], coords[end])
        if d > dmax:
            index = i
            dmax = d
            
    if dmax > epsilon:
        results1 = rdp(coords[:index+1], epsilon)
        results2 = rdp(coords[index:], epsilon)
        return results1[:-1] + results2
    else:
        return [coords[0], coords[end]]

def simplify_geometry(geom, epsilon):
    """Recursively simplify GeoJSON geometry coordinates."""
    g_type = geom["type"]
    coords = geom["coordinates"]
    
    if g_type == "Polygon":
        new_coords = []
        for ring in coords:
            if len(ring) > 2:
                simplified = rdp(ring, epsilon)
                # A valid polygon ring must have at least 4 coordinates (start == end)
                if len(simplified) < 4:
                    simplified = [ring[0], ring[len(ring)//3], ring[2*len(ring)//3], ring[0]]
                new_coords.append(simplified)
            else:
                new_coords.append(ring)
        return {"type": "Polygon", "coordinates": new_coords}
        
    elif g_type == "MultiPolygon":
        new_coords = []
        for poly in coords:
            new_poly = []
            for ring in poly:
                if len(ring) > 2:
                    simplified = rdp(ring, epsilon)
                    if len(simplified) < 4:
                        simplified = [ring[0], ring[len(ring)//3], ring[2*len(ring)//3], ring[0]]
                    new_poly.append(simplified)
                else:
                    new_poly.append(ring)
            new_coords.append(new_poly)
        return {"type": "MultiPolygon", "coordinates": new_coords}
        
    return geom

# --- MAIN SEEDING AND OPTIMIZATION PROCESS ---

def run_simplified_seeding():
    db = SessionLocal()
    try:
        print("="*60)
        print("RUNNING GEOSPATIAL SIMPLIFICATION & DB SEEDING")
        print("="*60)
        
        # 1. Clear old tables
        print("Clearing old territorial and relationship data...")
        db.execute(text("DELETE FROM project_territories"))
        db.execute(text("DELETE FROM prioritization_scores"))
        db.execute(text("DELETE FROM territories"))
        db.commit()
        
        # 2. Insert Country: Chile
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
        print("Added Country: Chile")
        
        # 3. Load & Simplify Regional.json (Epsilon: 0.002 ~220m resolution)
        reg_path = os.path.join(backend_dir, "..", "insumos", "datos_geo", "Regional.json")
        print(f"Loading regions from {reg_path}...")
        with open(reg_path, "r", encoding="utf-8") as f:
            reg_data = json.load(f)
            
        region_map = {}
        region_epsilon = 0.002
        print(f"Simplifying regions with RDP (epsilon={region_epsilon})...")
        
        for feat in reg_data["features"]:
            props = feat["properties"]
            geom = feat["geometry"]
            
            codregion = str(props["codregion"])
            name = props["Region"]
            
            # Area
            st_area = props.get("st_area_sh", 0)
            area_km = props.get("area_km", 0)
            area_ha = (st_area / 10000.0) if st_area else (area_km * 100.0)
            
            # Simplify geometry
            optimized_geom = simplify_geometry(geom, region_epsilon)
            
            reg_obj = Territory(
                code=f"CL-{codregion.zfill(2)}",
                name=name,
                type="region",
                parent_id=chile_id,
                geom_geojson=json.dumps(optimized_geom),
                area_ha=area_ha,
                is_sample=False
            )
            db.add(reg_obj)
            db.flush()
            region_map[codregion] = reg_obj
            print(f"  Loaded: {name} (CL-{codregion.zfill(2)})")
            
        # 4. Load & Simplify comunas.json (Epsilon: 0.001 ~110m resolution)
        com_path = os.path.join(backend_dir, "..", "insumos", "datos_geo", "comunas.json")
        print(f"Loading communes from {com_path}...")
        with open(com_path, "r", encoding="utf-8") as f:
            com_data = json.load(f)
            
        commune_epsilon = 0.001
        print(f"Simplifying 346 communes with RDP (epsilon={commune_epsilon})...")
        
        random.seed(42)
        commune_count = 0
        
        for feat in com_data["features"]:
            props = feat["properties"]
            geom = feat["geometry"]
            
            cod_comuna = str(props["cod_comuna"])
            name = props["Comuna"]
            codregion = str(props["codregion"])
            
            parent = region_map.get(codregion)
            parent_id = parent.id if parent else None
            
            # Area
            st_area = props.get("st_area_sh", 0)
            area_ha = (st_area / 10000.0) if st_area else 1000.0
            
            # Simplify geometry
            optimized_geom = simplify_geometry(geom, commune_epsilon)
            
            com_obj = Territory(
                code=cod_comuna.zfill(5),
                name=name,
                type="commune",
                parent_id=parent_id,
                geom_geojson=json.dumps(optimized_geom),
                area_ha=area_ha,
                is_sample=False
            )
            db.add(com_obj)
            db.flush()
            commune_count += 1
            
            # Generate Prioritization Score
            sf = round(random.uniform(30, 95), 1)
            # Regional flavor for Climate Risk (North vs South)
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
        print(f"\n[OK] Seeding complete! loaded {len(region_map)} optimized regions and {commune_count} optimized communes!")
        
    except Exception as e:
        db.rollback()
        print(f"\n[ERROR] Seeding failed: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    run_simplified_seeding()
