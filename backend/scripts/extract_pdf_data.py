"""Utility script to extract financial mechanisms from the provided PDF."""
import json
import re
try:
    import PyPDF2
except ImportError:
    print("Please install PyPDF2 (pip install PyPDF2)")
    exit(1)

def extract_mechanisms(pdf_path, output_json):
    print(f"Extracting mechanisms from {pdf_path}...")
    reader = PyPDF2.PdfReader(open(pdf_path, 'rb'))
    
    text = ""
    # Extract the first few pages where the index/summary usually is
    for i in range(1, min(10, len(reader.pages))):
        text += reader.pages[i].extract_text() + "\n"
    
    # Simple regex to find headings related to initiatives or mechanisms
    # Matches patterns like "Iniciativa 1: ...", "Mecanismo: ..." or capitalized titles
    pattern = r'(?:Iniciativa|Mecanismo)\s*\d*[:\-]?\s*([A-Z].+?)(?=\n|$)'
    matches = re.findall(pattern, text)
    
    # Deduplicate and clean
    mechanisms = []
    seen = set()
    for m in matches:
        clean_name = m.strip()
        if clean_name not in seen and len(clean_name) > 10:
            seen.add(clean_name)
            mechanisms.append({
                "name": clean_name,
                "category": "mecanismo_financiero",
                "description": "Extraído automáticamente del documento PDF."
            })
    
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump({"mechanisms": mechanisms}, f, ensure_ascii=False, indent=2)
    
    print(f"Extraction complete! Found {len(mechanisms)} potential mechanisms.")
    print(f"Saved to {output_json}")

if __name__ == "__main__":
    pdf_file = "../../insumos/documentos/8.2. INICIATIVAS PARA CHILE [Detalle].pdf"
    out_file = "../../insumos/documentos/mechanisms.json"
    extract_mechanisms(pdf_file, out_file)
