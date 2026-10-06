import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from typing import Optional
from app.config import UPLOAD_DIR
from app.api.schemas import QueryRequest, QueryResponse, EntityStatusUpdate, CompareRequest
from app.core.pdf_parser import extract_pdf_chunks, extract_raw_page_text
from app.core.rag_engine import rag_engine
from app.core.entity_extractor import extract_autosar_entities_from_pages
from app.core.comparator import compare_hld_revisions
from app.core.database import (
    register_document, save_extracted_entity, get_all_documents,
    get_all_audit_logs, get_extracted_entities, update_entity_status,
    log_audit_action
)

router = APIRouter()

@router.post("/ingest")
async def ingest_document(file: UploadFile = File(...), version: str = Form("v1.0")):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF documents are supported.")

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    chunks = extract_pdf_chunks(file_path)
    pages  = extract_raw_page_text(file_path)

    indexed_count = rag_engine.index_document_chunks(chunks, file.filename)

    register_document(file.filename, file_path, version=version, total_pages=len(pages))

    extracted_entities = extract_autosar_entities_from_pages(pages, file.filename)
    for entity in extracted_entities:
        save_extracted_entity(
            doc_name=entity["document_name"],
            entity_type=entity["entity_type"],
            entity_name=entity["entity_name"],
            description=entity["description"],
            page=entity["source_page"]
        )

    log_audit_action(
        action="DOCUMENT_INGEST",
        query_text=f"Uploaded {file.filename}",
        response_text=f"Indexed {indexed_count} chunks and extracted {len(extracted_entities)} entities.",
        citations=[],
        confidence=1.0
    )

    return {
        "status": "success",
        "filename": file.filename,
        "indexed_chunks": indexed_count,
        "extracted_entities_count": len(extracted_entities)
    }

@router.post("/query", response_model=QueryResponse)
async def query_knowledge_base(request: QueryRequest):
    answer, citations, confidence = rag_engine.query(request.query, top_k=request.top_k)

    log_audit_action(
        action="NATURAL_LANGUAGE_QUERY",
        query_text=request.query,
        response_text=answer,
        citations=citations,
        confidence=confidence
    )

    return QueryResponse(
        query=request.query,
        answer=answer,
        citations=citations,
        confidence_score=confidence
    )

@router.get("/documents")
async def list_documents():
    return get_all_documents()

@router.get("/entities")
async def list_entities(doc_name: Optional[str] = None):
    return get_extracted_entities(doc_name)

@router.post("/entity/review")
async def review_entity(update: EntityStatusUpdate):
    update_entity_status(update.entity_id, update.status)
    return {"status": "updated", "id": update.entity_id, "new_status": update.status}

@router.post("/compare")
async def compare_documents(request: CompareRequest):
    entities1 = get_extracted_entities(request.doc1_name)
    entities2 = get_extracted_entities(request.doc2_name)
    result = compare_hld_revisions(entities1, entities2, request.doc1_name, request.doc2_name)

    log_audit_action(
        action="REVISION_COMPARISON",
        query_text=f"Comparing {request.doc1_name} vs {request.doc2_name}",
        response_text=f"Found {len(result['inconsistencies'])} differences.",
        citations=[],
        confidence=1.0
    )

    return result

@router.get("/audit_logs")
async def get_audit_logs():
    return get_all_audit_logs()
