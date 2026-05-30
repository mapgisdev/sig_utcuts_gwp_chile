import httpx
import json
import os
import time
from shapely.geometry import shape, mapping

url_base = "https://esri.ciren.cl/server/rest/services/IDEMINAGRI/RECURSOS_FORESTALES/MapServer"
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "insumos", "datos_geo"))
output_file = os.path.join(output_dir, "plantaciones_forestales_2022.json")

LAYER_TO_REGION = {
    79: "04", # Coquimbo
    80: "05", # Valparaíso
    81: "13", # Metropolitana
    82: "06", # O'Higgins
    83: "07", # Maule
    84: "16", # Ñuble
    85: "08", # Biobío
    86: "09", # Araucanía
    87: "14", # Los Ríos
    88: "10", # Los Lagos
    89: "11"  # Aysén
}

def simplify_geom(geojson_geom):
    try:
        sh = shape(geojson_geom)
        simplified = sh.simplify(0.0005, preserve_topology=False)
        return mapping(simplified)
    except Exception:
        return geojson_geom

def fetch_batch_with_retry(query_url, offset, start_batch_size):
    retries = 3
    current_batch_size = start_batch_size
    while current_batch_size >= 50:
        for attempt in range(retries):
            params = {
                "where": "1=1",
                "outFields": "objectid,especie_t,apl,sup_ha",
                "outSR": "4326",
                "resultOffset": offset,
                "resultRecordCount": current_batch_size,
                "f": "geojson"
            }
            try:
                # Use a larger timeout of 45 seconds to accommodate slow server responses
                r = httpx.get(query_url, params=params, timeout=45.0)
                if r.status_code == 200:
                    data = r.json()
                    features = data.get("features", [])
                    return features, current_batch_size
                else:
                    print(f"  [WARN] Attempt {attempt+1} returned status {r.status_code}. Retrying...", flush=True)
            except Exception as e:
                print(f"  [WARN] Attempt {attempt+1} failed: {e}. Retrying...", flush=True)
            time.sleep(2)
        # Halve batch size and try again
        current_batch_size = current_batch_size // 2
        print(f"  [INFO] Halving batch size to {current_batch_size} due to repeated timeouts/failures.", flush=True)
    return None, current_batch_size

def main():
    os.makedirs(output_dir, exist_ok=True)
    print(f"Target output path: {output_file}", flush=True)
    
    combined_geojson = {
        "type": "FeatureCollection",
        "features": []
    }
    
    for lid, reg_code in LAYER_TO_REGION.items():
        print(f"\nProcessing Layer ID {lid} (Region {reg_code})...", flush=True)
        offset = 0
        batch_size = 500  # Start with 500 features per query for safety and speed
        
        while True:
            query_url = f"{url_base}/{lid}/query"
            features, active_batch_size = fetch_batch_with_retry(query_url, offset, batch_size)
            
            if features is None:
                print(f"  [ERROR] Failed to query batch at offset {offset} even with minimal batch size. Skipping rest of layer {lid}.", flush=True)
                break
                
            if not features:
                break
                
            print(f"  Fetched batch of {len(features)} features at offset {offset} (batch size {active_batch_size})", flush=True)
            
            for feat in features:
                props = feat.setdefault("properties", {})
                props["codreg"] = reg_code
                
                geom = feat.get("geometry")
                if geom:
                    feat["geometry"] = simplify_geom(geom)
                    
                combined_geojson["features"].append(feat)
                
            offset += len(features)
            if len(features) < active_batch_size:
                break # Last batch
                
    print(f"\nTotal compiled features across all layers: {len(combined_geojson['features'])}", flush=True)
    
    if len(combined_geojson["features"]) > 0:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(combined_geojson, f, indent=2, ensure_ascii=False)
        print("Successfully wrote combined simplified forest plantations GeoJSON file.", flush=True)
    else:
        print("[ERROR] No features downloaded. File was not created.", flush=True)

if __name__ == '__main__':
    main()
