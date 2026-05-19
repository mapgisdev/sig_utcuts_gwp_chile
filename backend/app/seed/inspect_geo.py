import json

def inspect():
    paths = {
        "comunas": r"C:\web_antigravity\web_D_gemini\sig_utcuts_gwp_chile\insumos\datos_geo\comunas.json",
        "areas_protegidas": r"C:\web_antigravity\web_D_gemini\sig_utcuts_gwp_chile\insumos\datos_geo\Areas_Protegidas.json",
        "acuicultura": r"C:\web_antigravity\web_D_gemini\sig_utcuts_gwp_chile\insumos\datos_geo\Concesiones_Acuicultura_geo.json"
    }
    
    # 1. Comunas
    print("Reading comunas.json...")
    with open(paths["comunas"], "r", encoding="utf-8") as f:
        data = json.load(f)
    print(f"Comunas total features: {len(data.get('features', []))}")
    if data.get('features'):
        print("Sample Comuna props:", data['features'][0]['properties'])
        
    # 2. Areas Protegidas
    print("\nReading Areas_Protegidas.json...")
    with open(paths["areas_protegidas"], "r", encoding="utf-8") as f:
        data_ap = json.load(f)
    print(f"Areas Protegidas total features: {len(data_ap.get('features', []))}")
    if data_ap.get('features'):
        print("Sample Area Protegida props:", data_ap['features'][0]['properties'])

    # 3. Acuicultura
    print("\nReading Concesiones_Acuicultura_geo.json...")
    with open(paths["acuicultura"], "r", encoding="utf-8") as f:
        data_ac = json.load(f)
    print(f"Acuicultura total features: {len(data_ac.get('features', []))}")
    if data_ac.get('features'):
        print("Sample Acuicultura props:", data_ac['features'][0]['properties'])

if __name__ == "__main__":
    inspect()
