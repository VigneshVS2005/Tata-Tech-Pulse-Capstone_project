from typing import List, Dict, Any

def compare_hld_revisions(doc1_entities: List[Dict[str, Any]], doc2_entities: List[Dict[str, Any]], doc1_name: str, doc2_name: str) -> Dict[str, Any]:
    set1 = {(e["entity_type"], e["entity_name"]) for e in doc1_entities}
    set2 = {(e["entity_type"], e["entity_name"]) for e in doc2_entities}
    
    added = set2 - set1
    removed = set1 - set2
    common = set1 & set2
    
    inconsistencies = []
    
    for entity_type, entity_name in added:
        inconsistencies.append({
            "type": "Added Entity",
            "entity_type": entity_type,
            "entity_name": entity_name,
            "details": f"New symbol '{entity_name}' ({entity_type}) present in {doc2_name} but missing in {doc1_name}.",
            "severity": "Medium"
        })
        
    for entity_type, entity_name in removed:
        inconsistencies.append({
            "type": "Removed / Deprecated Entity",
            "entity_type": entity_type,
            "entity_name": entity_name,
            "details": f"Symbol '{entity_name}' ({entity_type}) present in {doc1_name} but removed in {doc2_name}.",
            "severity": "High" if entity_type in ("SoftwareComponent", "Interface") else "Medium"
        })
        
    return {
        "doc1": doc1_name,
        "doc2": doc2_name,
        "summary": {
            "total_doc1_entities": len(set1),
            "total_doc2_entities": len(set2),
            "common_entities": len(common),
            "added_count": len(added),
            "removed_count": len(removed)
        },
        "inconsistencies": inconsistencies
    }
