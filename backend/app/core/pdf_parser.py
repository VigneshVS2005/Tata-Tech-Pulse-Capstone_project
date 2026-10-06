import pymupdf  # PyMuPDF
import re
from typing import List, Dict, Any

def extract_pdf_chunks(pdf_path: str) -> List[Dict[str, Any]]:
    """
    Parses a PDF document page-by-page, extracts text, headings, and generates context-aware chunks.
    """
    doc = pymupdf.open(pdf_path)
    chunks = []
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text("text").strip()
        if not text:
            continue
            
        # Split text into sections or paragraphs
        paragraphs = text.split("\n\n")
        current_section = f"Page {page_num + 1}"
        
        for p_idx, para in enumerate(paragraphs):
            para_clean = para.strip()
            if not para_clean:
                continue
                
            # Check for heading heuristic (short line, capital letters)
            lines = para_clean.split("\n")
            if len(lines[0]) < 60 and (lines[0].isupper() or lines[0].istitle() or re.match(r'^\d+(\.\d+)*', lines[0])):
                current_section = lines[0]
                
            chunk_data = {
                "text": para_clean,
                "metadata": {
                    "page": page_num + 1,
                    "section": current_section,
                    "chunk_id": f"p{page_num + 1}_c{p_idx + 1}"
                }
            }
            chunks.append(chunk_data)
            
    doc.close()
    return chunks

def extract_raw_page_text(pdf_path: str) -> List[Dict[str, Any]]:
    doc = pymupdf.open(pdf_path)
    pages = []
    for page_num in range(len(doc)):
        page = doc[page_num]
        pages.append({
            "page": page_num + 1,
            "text": page.get_text("text").strip()
        })
    doc.close()
    return pages
