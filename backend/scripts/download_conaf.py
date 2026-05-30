import urllib.request
import zipfile
import os
import ssl

URL = "https://sit.conaf.cl/archivos/Catastro_Bosque_Nativo_Aysen.zip"

OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "insumos", "datos_geo", "descargas"))
ZIP_PATH = os.path.join(OUTPUT_DIR, "catastro_aysen.zip")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Directorio de descarga preparado: {OUTPUT_DIR}")
    print(f"Iniciando descarga desde: {URL}")
    
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    req = urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    
    try:
        with urllib.request.urlopen(req, context=ctx) as response, open(ZIP_PATH, 'wb') as out_file:
            data = response.read()
            out_file.write(data)
        print("Descarga completada con éxito.")
        
        print("Extrayendo archivos...")
        with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
            zip_ref.extractall(OUTPUT_DIR)
        print(f"Archivos extraídos correctamente en: {OUTPUT_DIR}")
        
    except urllib.error.HTTPError as e:
        print(f"Error HTTP al descargar: {e.code} {e.reason}")
        print("Verifica si el enlace ha expirado y genera uno nuevo en sit.conaf.cl")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

if __name__ == '__main__':
    main()
