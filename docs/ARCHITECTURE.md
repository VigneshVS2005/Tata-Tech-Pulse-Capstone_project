# Automotive Engineering AI Platform
## Tata Tech Pulse - Digital Track (Case Study 1)

### Executive Summary & Alignment
This repository implements **Case Study 1: AUTOSAR HLD Document Analysis Assistant** as outlined in the Tata Technologies Automotive Engineering AI standard specification.

The platform provides an evidence-backed Retrieval-Augmented Generation (RAG) system for ingesting unstructured AUTOSAR High-Level Design (HLD) PDFs, parsing architectural components/interfaces, conducting natural language queries with grounded citations, detecting revision inconsistencies, and maintaining a strict governance audit log.

---

### Key Capabilities & Criteria Checklist

| Requirement Criteria in PDF | Implementation Feature in Platform | Status |
|---|---|---|
| **Document Ingestion & OCR** | PyMuPDF page parsing and context-aware paragraph chunking | ✅ Complete |
| **Vector Storage & Retrieval** | Persistent local ChromaDB with SentenceTransformers (`all-MiniLM-L6-v2`) | ✅ Complete |
| **AUTOSAR Entity Extraction** | Regex & pattern recognition for SWCs, Interfaces, Ports, and Signals | ✅ Complete |
| **Grounded Q&A with Citations** | RAG query pipeline providing exact page, section, and confidence score citations | ✅ Complete |
| **Revision Comparison** | Automated delta analysis comparing HLD v1.0 vs v2.0 to detect added/removed symbols | ✅ Complete |
| **Governance & Audit Trail** | SQLite database logging all queries, citations, confidence scores, & review decisions | ✅ Complete |
| **Engineering User Interface** | Multi-tab Streamlit Web Application backed by a modular FastAPI service layer | ✅ Complete |

---

### Project Architecture

```
[ ENGINEERING USER ]
         |
         v
 [ STREAMLIT UI ] (frontend/app.py)
         |  (REST API calls)
         v
 [ FASTAPI BACKEND ] (backend/app/main.py)
   +---> [ PDF Parser ] (PyMuPDF chunking)
   +---> [ Vector Store ] (ChromaDB + SentenceTransformers)
   +---> [ Entity Extractor ] (AUTOSAR SWCs, Ports, Signals)
   +---> [ Revision Comparator ] (Delta & inconsistency check)
   +---> [ SQLite Database ] (Document registry, entity status, audit log)
```

---

### How to Run the Platform

1. **Activate Virtual Environment:**
   ```powershell
   .\venv\Scripts\activate
   ```
2. **Launch Both Backend & Frontend:**
   ```powershell
   python run_app.py
   ```
3. **Access Services:**
   - **Streamlit App:** http://localhost:8501
   - **FastAPI API Docs:** http://127.0.0.1:8000/docs

   4. **hosted**
   - **Streamlit App:**  https://tata-tech-pulse-capstoneproject-vigneshvs.streamlit.app/
   - **github repo:**  https://github.com/VigneshVS2005/Tata-Tech-Pulse-Capstone_project
