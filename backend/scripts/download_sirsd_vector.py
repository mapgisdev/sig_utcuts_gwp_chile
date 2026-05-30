import httpx
import json
import os
import time

url_base = "https://esri.ciren.cl/server/rest/services/IDEMINAGRI/PROG_RECUPERACION_SUELOS_DEGRA/MapServer"
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "insumos", "datos_geo"))
output_file = os.path.join(output_dir, "prog_recuperacion_suelos_degra.json")

def main():
    os.makedirs(output_dir, exist_ok=True)
    print(f"Target output path: {output_file}", flush=True)
    
    combined_geojson = {
        "type": "FeatureCollection",
        "features": []
    }
    
    # Query layer IDs 24 to 33 (Concursos 01 al 10 de 2024)
    for lid in range(24, 34):
        print(f"Downloading vector features for Layer ID {lid}...", flush=True)
        query_url = f"{url_base}/{lid}/query"
        params = {
            "where": "1=1",
            "outFields": "*",
            "outSR": "4326",
            "f": "geojson"
        }
        
        try:
            r = httpx.get(query_url, params=params, timeout=40.0)
            if r.status_code == 200:
                data = r.json()
                features = data.get("features", [])
                print(f"  Successfully fetched {len(features)} features.", flush=True)
                
                for feat in features:
                    props = feat.setdefault("properties", {})
                    props["sublayer_id"] = lid
                    combined_geojson["features"].append(feat)
            else:
                print(f"  [ERROR] Layer {lid} returned status code {r.status_code}", flush=True)
        except Exception as e:
            print(f"  [ERROR] Failed to download Layer {lid}: {e}", flush=True)
            
    print(f"Total compiled features: {len(combined_geojson['features'])}", flush=True)
    
    if len(combined_geojson["features"]) > 0:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(combined_geojson, f, indent=2, ensure_ascii=False)
        print("Successfully wrote combined GeoJSON file.", flush=True)
    else:
        print("[ERROR] No features downloaded. File was not created.", flush=True)

if __name__ == '__main__':
    main()
