"""Inspect PDF 2 — targets Linea_Base_Financiamiento_UTCUTS_v2_2.pdf specifically."""
import os
import sys
from pypdf import PdfReader

backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(backend_dir)

def inspect_pdf(file_path):
    print("="*80)
    print(f"📖 INSPECTING: {os.path.basename(file_path)}")
    print("="*80)
    
    if not os.path.exists(file_path):
        print("  [Error] File does not exist.")
        return
        
    reader = PdfReader(file_path)
    total_pages = len(reader.pages)
    print(f"  Total Pages: {total_pages}\n")
    
    # 1. Print first 6 pages (covers and introductory index)
    print("--- [Introductory Pages Text Sample] ---")
    intro_limit = min(6, total_pages)
    for i in range(intro_limit):
        text = reader.pages[i].extract_text()
        print(f"\n[PAGE {i+1}]:")
        print(text[:1200] + ("..." if len(text) > 1200 else ""))
        
    # 2. Search for tables or candidate financial numbers pages
    print("\n--- [Searching for Key Keywords: 'brecha', 'financiamiento', 'monto', 'costo', 'tabla', 'usd', 'millones', 'inversión'] ---")
    keywords = ["brecha", "financiamiento", "monto", "costo", "tabla", "usd", "millones", "inversión"]
    matches = []
    
    for page_idx in range(total_pages):
        text = reader.pages[page_idx].extract_text().lower()
        found = [k for k in keywords if k in text]
        if found:
            matches.append((page_idx + 1, found))
            
    print(f"  Found potential keyword matches in {len(matches)} pages.")
    prominent = sorted(matches, key=lambda x: len(x[1]), reverse=True)[:6]
    print("\n  Prominent Pages for data extraction:")
    for page_num, kw_list in prominent:
        print(f"    - Page {page_num}: Keywords matched: {kw_list}")
        
    # Print the full content of the most prominent page
    if prominent:
        best_page = prominent[0][0]
        print(f"\n--- [Full Text of Most Relevant Page: Page {best_page}] ---")
        print(reader.pages[best_page - 1].extract_text())

if __name__ == "__main__":
    docs_dir = os.path.join(backend_dir, "..", "insumos", "documentos")
    inspect_pdf(os.path.join(docs_dir, "Linea_Base_Financiamiento_UTCUTS_v2_2.pdf"))
