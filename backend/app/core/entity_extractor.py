import re
from typing import List, Dict, Any

# Pattern matching rules for AUTOSAR domain entities
AUTOSAR_PATTERNS = {
    "SoftwareComponent": [
        r'\b([A-Z][a-zA-Z0-9_]*(?:Swc|Component|Manager|Controller|Handler|Module))\b',
        r'Component:\s*([A-Za-z0-9_]+)',
        r'SWC:\s*([A-Za-z0-9_]+)'
    ],
    "Interface": [
        r'\b(If_[A-Za-z0-9_]+)\b',
        r'\b(PortIf_[A-Za-z0-9_]+)\b',
        r'Interface:\s*([A-Za-z0-9_]+)',
        r'\b([A-Z][a-zA-Z0-9_]*Interface)\b'
    ],
    "Port": [
        r'\b(PPort_[A-Za-z0-9_]+)\b',
        r'\b(RPort_[A-Za-z0-9_]+)\b',
        r'Port:\s*([A-Za-z0-9_]+)'
    ],
    "Signal": [
        r'\b(Sig_[A-Za-z0-9_]+)\b',
        r'\b(S_([A-Z][a-zA-Z0-9_]+))\b',
        r'Signal:\s*([A-Za-z0-9_]+)'
    ]
}

def extract_autosar_entities_from_pages(pages: List[Dict[str, Any]], doc_name: str) -> List[Dict[str, Any]]:
    extracted = []
    seen = set()
    
    for page_info in pages:
        page_num = page_info["page"]
        text = page_info["text"]
        
        for entity_type, patterns in AUTOSAR_PATTERNS.items():
            for pattern in patterns:
                matches = re.findall(pattern, text)
                for match in matches:
                    entity_name = match[0] if isinstance(match, tuple) else match
                    entity_name = entity_name.strip()
                    
                    # Filter out short or non-domain matches
                    if len(entity_name) < 3 or entity_name in ("The", "And", "For", "With", "Interface", "Component"):
                        continue
                        
                    key = (entity_type, entity_name)
                    if key not in seen:
                        seen.add(key)
                        extracted.append({
                            "document_name": doc_name,
                            "entity_type": entity_type,
                            "entity_name": entity_name,
                            "description": f"Extracted from {doc_name} on page {page_num}",
                            "source_page": page_num,
                            "review_status": "pending_review"
                        })
                        
    return extracted
