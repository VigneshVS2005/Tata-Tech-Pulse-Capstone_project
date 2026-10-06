# 🚗 Automotive Engineering AI Platform
## Tata Tech Pulse — Digital Track | Case Study 1: AUTOSAR HLD Analysis Assistant

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.38-red)](https://streamlit.io/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-0.5-blue)](https://www.trychroma.com/)
[![Python](https://img.shields.io/badge/Python-3.13-yellow)](https://www.python.org/)

### 🔗 Live Demo
- **Web Application (UI):** *(Deployed on Streamlit Cloud)*
- **API Documentation:** *(Deployed on Render)*

---

### 📋 Project Overview

An evidence-backed **Retrieval-Augmented Generation (RAG)** platform for automotive software engineers to:

- Upload AUTOSAR High-Level Design (HLD) PDF documents
- Extract and inventory software components, interfaces, ports & signals automatically
- Ask natural language queries with grounded citations (page number, section, relevance score)
- Compare revisions of HLD documents to detect architectural inconsistencies
- Maintain a full governance audit log for traceability

---

### 🏗️ Architecture

```
[ Engineer ] → [ Streamlit UI ] → [ FastAPI Backend ] → [ ChromaDB Vector Store ]
                                                     ↘ [ SQLite Audit DB ]
```

---

### 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | Streamlit |
| **Backend API** | FastAPI + Uvicorn |
| **Vector Database** | ChromaDB (local persistent) |
| **Embeddings** | SentenceTransformers (`all-MiniLM-L6-v2`) with TF-IDF fallback |
| **PDF Parsing** | PyMuPDF |
| **Entity Extraction** | Regex-based AUTOSAR pattern matching |
| **Audit Storage** | SQLite |
| **Hosting** | Render (Backend) + Streamlit Community Cloud (Frontend) |

---

### 🚀 Run Locally

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt

# 3. Launch both services
python run_app.py
```

- **API Docs:** http://127.0.0.1:8000/docs
- **Streamlit UI:** http://localhost:8501

---

### 📁 Project Structure

```
├─ backend/            # FastAPI backend service
│   ├─ app/
│   │   ├─ main.py     # FastAPI entrypoint
│   │   ├─ config.py   # Paths & settings
│   │   ├─ core/
│   │   │   ├─ pdf_parser.py       # PyMuPDF-based chunker
│   │   │   ├─ rag_engine.py       # ChromaDB RAG pipeline
│   │   │   ├─ entity_extractor.py # AUTOSAR entity extractor
│   │   │   ├─ comparator.py       # Revision delta checker
│   │   │   └─ database.py         # SQLite audit log
│   │   └─ api/
│   │       ├─ endpoints.py        # REST API routes
│   │       └─ schemas.py          # Pydantic schemas
│   └─ requirements.txt
├─ frontend/           # Streamlit web interface
│   ├─ app.py          # Multi-tab Streamlit dashboard
│   └─ requirements.txt
├─ sample_data/        # Example AUTOSAR HLD PDFs
├─ docs/
│   └─ ARCHITECTURE.md # Detailed technical documentation
└─ run_app.py          # Local launcher script
```

---

### 📊 Submission Checklist

| Requirement | Status |
|---|---|
| Document Ingestion (PDF → text chunks) | ✅ |
| Vector Storage & Semantic Search | ✅ |
| AUTOSAR Entity Extraction | ✅ |
| Grounded Q&A with Page Citations | ✅ |
| HLD Revision Comparison | ✅ |
| Governance Audit Trail | ✅ |
| Web UI (Streamlit) | ✅ |
| REST API (FastAPI + Swagger) | ✅ |
| Dockerized Deployment | ✅ |
| CI/CD (GitHub Actions) | ✅ |
