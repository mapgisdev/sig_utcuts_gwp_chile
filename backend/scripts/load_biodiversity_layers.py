import os
import sys
import json
from shapely.geometry import shape

# Configurar el path para poder importar módulos de la app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.db.session import SessionLocal
from app.models.territory import Territory
from app.models.layer import Layer
from app.models.prioritization import PrioritizationScore

def load_layers():
    db = SessionLocal()
    try:
        # 1. Asegurar que las capas existan en el catálogo
        areas_layer = db.query(Layer).filter(Layer.name == "Áreas Protegidas").first()
        if not areas_layer:
            areas_layer = Layer(
                name="Áreas Protegidas",
                description="Áreas terrestres y marinas protegidas de Chile (SIMBIO)",
                category="biodiversity",
                layer_type="geojson",
                geometry_type="polygon",
                is_active=True,
                is_official=True,
                is_sample=False
            )
            db.add(areas_layer)

        ecmpo_layer = db.query(Layer).filter(Layer.name == "Espacios Costeros Marinos (ECMPO)").first()
        if not ecmpo_layer:
            ecmpo_layer = Layer(
                name="Espacios Costeros Marinos (ECMPO)",
                description="Espacios Costeros Marinos de Pueblos Originarios en Chile",
                category="biodiversity",
                layer_type="geojson",
                geometry_type="polygon",
                is_active=True,
                is_official=True,
                is_sample=False
            )
            db.add(ecmpo_layer)
        db.commit()

        # Limpiar datos antiguos de tipo protected_area para evitar duplicados en la base de datos real
        print("  > Limpiando áreas protegidas antiguas...")
        db.query(Territory).filter(Territory.type == "protected_area").delete()
        db.commit()

        # 2. Cargar Áreas Protegidas
        ap_path = "/insumos/datos_geo/Areas_Protegidas.json"
        if os.path.exists(ap_path):
            print(f"  > Procesando {ap_path}...")
            with open(ap_path, "r", encoding="utf-8") as f:
                ap_data = json.load(f)
            
            count = 0
            for idx, feat in enumerate(ap_data.get("features", [])):
                props = feat.get("properties", {})
                geom_dict = feat.get("geometry")
                if not geom_dict:
                    continue
                
                try:
                    geom = shape(geom_dict)
                    name = props.get("NombreOrig") or f"Área Protegida {idx}"
                    code = f"AP-{idx:04d}"
                    
                    t = Territory(
                        code=code,
                        name=name,
                        type="protected_area",
                        geom=f"SRID=4326;{geom.wkt}"
                    )
                    db.add(t)
                    count += 1
                    if count % 50 == 0:
                        db.flush()
                except Exception as ex:
                    print(f"Error procesando elemento {idx} de áreas protegidas: {ex}")
            db.commit()
            print(f"  > Cargadas {count} áreas protegidas en PostGIS.")

        # 3. Cargar ECMPO
        ecmpo_path = "/insumos/datos_geo/ECMPO_geo.json"
        if os.path.exists(ecmpo_path):
            print(f"  > Procesando {ecmpo_path}...")
            with open(ecmpo_path, "r", encoding="utf-8") as f:
                ecmpo_data = json.load(f)
            
            count = 0
            for idx, feat in enumerate(ecmpo_data.get("features", [])):
                props = feat.get("properties", {})
                geom_dict = feat.get("geometry")
                if not geom_dict:
                    continue
                
                try:
                    geom = shape(geom_dict)
                    name = props.get("REP_SUBPES") or f"ECMPO {idx}"
                    code = f"EC-{idx:04d}"
                    
                    t = Territory(
                        code=code,
                        name=name,
                        type="protected_area",
                        geom=f"SRID=4326;{geom.wkt}"
                    )
                    db.add(t)
                    count += 1
                    if count % 50 == 0:
                        db.flush()
                except Exception as ex:
                    print(f"Error procesando elemento {idx} de ECMPO: {ex}")
            db.commit()
            print(f"  > Cargadas {count} áreas de ECMPO en PostGIS.")

    except Exception as e:
        db.rollback()
        print(f"Error durante la carga: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("Iniciando la ingesta de capas de biodiversidad...")
    load_layers()
    print("Ingesta completada.")
