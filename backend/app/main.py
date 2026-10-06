from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import init_db
from app.api.endpoints import router as api_router

app = FastAPI(
    title="Automotive Engineering AI - AUTOSAR HLD Platform",
    description="Evidence-based RAG and Architecture Knowledge Management API for AUTOSAR HLD Documents",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    init_db()

app.include_router(api_router, prefix="/api")

@app.get("/")
def root():
    return {
        "title": "Automotive Engineering AI Platform",
        "version": "1.0.0",
        "status": "online",
        "docs": "/docs"
    }
