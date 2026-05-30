import urllib.request
import json
import os

URL = "https://arclim.mma.gob.cl/api/datos/comunas/json"
ATTRIBUTES = [
    "ComCod",
    "NOM_COMUNA",
    "paarc_aysen_incendios_riesgo",
    "parcc_magallanes_biodiversidadturismo_humedales_riesgo_humedal",
    "parcc_magallanes_biodiversidadturismo_nothofagus_riesgo_nothofagus"
]

OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "insumos", "datos_geo", "descargas"))
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "arclim_riesgo.json")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Directorio de descarga preparado: {OUTPUT_DIR}")
    
    query_url = f"{URL}?attributes={','.join(ATTRIBUTES)}"
    print(f"Consultando API de ARClim: {query_url}")
    
    req = urllib.request.Request(query_url, headers={'User-Agent': 'Mozilla/5.0'})
    
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
        
        # Estructuramos la respuesta en un JSON limpio con pares clave-valor por comuna
        split_data = data.get('data', {})
        columns = split_data.get('columns', [])
        values = split_data.get('values', [])
        
        records = []
        for val in values:
            record = dict(zip(columns, val))
            # Omitir comunas sin código válido
            if record.get('ComCod'):
                # Convertir código numérico a formato CUD (5 caracteres con relleno de ceros)
                # ej. 1401.0 -> "01401"
                try:
                    cod_num = int(float(record['ComCod']))
                    record['ComCod_CUD'] = f"{cod_num:05d}"
                except Exception:
                    record['ComCod_CUD'] = str(record['ComCod'])
                records.append(record)
        
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
            
        print(f"[OK] Descarga de ARClim exitosa. Guardados {len(records)} registros en: {OUTPUT_FILE}")
        
    except urllib.error.HTTPError as e:
        print(f"[ERROR] Error HTTP al consultar ARClim: {e.code} {e.reason}")
    except Exception as e:
        print(f"[ERROR] Ocurrió un error inesperado: {e}")

if __name__ == '__main__':
    main()
