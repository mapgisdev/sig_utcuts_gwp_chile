"""Extract PDF Details — pulls exact tables and text from targeted pages of both PDFs."""
import os
import sys
from pypdf import PdfReader

backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(backend_dir)

def extract_pages(file_name, pages):
    docs_dir = os.path.join(backend_dir, "..", "insumos", "documentos")
    file_path = os.path.join(docs_dir, file_name)
    
    print("\n" + "="*80)
    print(f"📄 EXTRACTING PAGES FROM: {file_name}")
    print("="*80)
    
    if not os.path.exists(file_path):
        print(f"  [Error] File not found: {file_path}")
        return
        
    reader = PdfReader(file_path)
    for p in pages:
        if p <= len(reader.pages):
            print(f"\n--- [PAGE {p}] ---")
            print(reader.pages[p - 1].extract_text())
        else:
            print(f"\n--- [PAGE {p}] (Out of range) ---")

if __name__ == "__main__":
    # 1. Extract initiatives details from 8.2. INICIATIVAS PARA CHILE [Detalle].pdf
    # Page 9: Síntesis de las 10 iniciativas, Page 11-13: Fichas de iniciativas
    extract_pages("8.2. INICIATIVAS PARA CHILE [Detalle].pdf", [9, 10, 11, 12, 13])
    
    # 2. Extract financial details from Linea_Base_Financiamiento_UTCUTS_v2_2.pdf
    # Page 16: Instrumentos públicos chilenos, Page 17: Cooperación internacional, Page 19: ENCCRV Plan, Page 21: Costos unitarios, Page 23: Inversión privada
    extract_pages("Linea_Base_Financiamiento_UTCUTS_v2_2.pdf", [16, 17, 19, 21, 23])
