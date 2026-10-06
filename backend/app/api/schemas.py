from pydantic import BaseModel
from typing import List, Optional, Any

class QueryRequest(BaseModel):
    query: str
    top_k: Optional[int] = 4

class QueryResponse(BaseModel):
    query: str
    answer: str
    citations: List[Any]
    confidence_score: float

class EntityStatusUpdate(BaseModel):
    entity_id: int
    status: str # approved, rejected, pending_review

class CompareRequest(BaseModel):
    doc1_name: str
    doc2_name: str
