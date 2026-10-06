import os
import streamlit as st
import requests
import pandas as pd

# Backend URL — reads from env var set by Streamlit Cloud, falls back to live Render backend
API_BASE_URL = os.environ.get("API_BASE_URL", "https://tata-tech-pulse-backend.onrender.com/api")

st.set_page_config(
    page_title="Automotive Engineering AI Platform",
    page_icon="🚘",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    .main-header {
        font-size: 2.4rem;
        font-weight: 700;
        color: #0F4C81;
        margin-bottom: 0px;
        letter-spacing: -0.5px;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #666;
        margin-bottom: 28px;
    }
    .metric-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 12px;
        padding: 18px 20px;
        border-left: 5px solid #0F4C81;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        height: 90px;
    }
    .metric-card h4 { margin: 0 0 6px 0; font-size: 0.8rem; color: #888; text-transform: uppercase; letter-spacing: 1px; }
    .metric-card p  { margin: 0; font-size: 0.95rem; font-weight: 600; color: #222; }
    .citation-box {
        background: #EBF3FA;
        border-radius: 8px;
        padding: 12px 16px;
        margin-top: 10px;
        border-left: 4px solid #1976D2;
        font-size: 0.88rem;
    }
    div[data-testid="stTabs"] button {
        font-weight: 600;
    }
    .badge-green  { background:#d4edda; color:#155724; padding:2px 8px; border-radius:12px; font-size:0.78rem; }
    .badge-orange { background:#fff3cd; color:#856404; padding:2px 8px; border-radius:12px; font-size:0.78rem; }
    .badge-red    { background:#f8d7da; color:#721c24; padding:2px 8px; border-radius:12px; font-size:0.78rem; }
</style>
""", unsafe_allow_html=True)

# ─── Sidebar ────────────────────────────────────────────────────────────────
st.sidebar.markdown("## 🚘 Tata Tech Pulse")
st.sidebar.markdown("**Digital Track — Case Study 1**")
st.sidebar.markdown("---")

backend_online = False
try:
    res = requests.get(API_BASE_URL.replace("/api", "/"), timeout=3)
    backend_online = res.status_code == 200
except Exception:
    pass

if backend_online:
    st.sidebar.success("⚡ Backend API: Connected")
else:
    st.sidebar.error("❌ Backend: Offline")

st.sidebar.markdown("---")
st.sidebar.markdown("""
**Stack**
- 🗄️ Vector DB: ChromaDB
- 🤖 Embeddings: SentenceTransformers
- ⚡ API: FastAPI
- 🖥️ UI: Streamlit
- 🏗️ Parsing: PyMuPDF
""")
st.sidebar.markdown("---")
st.sidebar.caption(f"API: `{API_BASE_URL}`")

# ─── Header ─────────────────────────────────────────────────────────────────
st.markdown('<p class="main-header">🚗 Automotive Engineering AI Platform</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">AUTOSAR High-Level Design (HLD) Document Analysis & Architecture Knowledge Assistant</p>', unsafe_allow_html=True)

# ─── Tabs ────────────────────────────────────────────────────────────────────
tabs = st.tabs([
    "📊 Overview",
    "📄 Upload & Ingest",
    "🔍 Grounded Q&A",
    "🧩 Component Inventory",
    "🔄 Revision Compare",
    "📜 Audit Log"
])

# ════════════════════════════════════════════════════════════════════════
# TAB 1 — OVERVIEW
# ════════════════════════════════════════════════════════════════════════
with tabs[0]:
    st.header("Executive Overview")

    col1, col2, col3, col4 = st.columns(4)
    cards = [
        ("Business Value", "Faster architecture analysis & knowledge reuse"),
        ("Vector Engine", "ChromaDB (Local Persistent Storage)"),
        ("RAG Pipeline", "SentenceTransformers + Evidence Synthesis"),
        ("Governance", "Page Citations + Engineer Approval Workflow"),
    ]
    for col, (title, body) in zip([col1, col2, col3, col4], cards):
        with col:
            st.markdown(f'<div class="metric-card"><h4>{title}</h4><p>{body}</p></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("What This Platform Does")
    st.markdown("""
    This application implements **Case Study 1: AUTOSAR HLD Document Analysis Assistant**
    from the Tata Technologies Automotive Engineering AI Project.

    | Capability | Description |
    |---|---|
    | **PDF Ingestion** | Upload AUTOSAR HLD design docs (any size) and auto-extract all text sections |
    | **Vector Search** | Semantic search across all uploaded documents using embeddings |
    | **Entity Extraction** | Auto-detect Software Components, Interfaces, Ports & Signals |
    | **Grounded Q&A** | Natural language queries with grounded page & section citations |
    | **Revision Comparison** | Compare HLD v1 vs v2 to detect added, removed, or changed architecture |
    | **Audit Trail** | Full log of every query, answer, citation & engineer review decision |
    """)

    st.markdown("---")
    st.subheader("Architecture Diagram")
    st.code("""
┌──────────────────┐    REST API    ┌──────────────────────────────────────┐
│  Streamlit UI    │ ─────────────► │  FastAPI Backend                     │
│  (this page)     │                │  ├─ /api/ingest  (PDF → ChromaDB)    │
└──────────────────┘                │  ├─ /api/query   (RAG Q&A)           │
                                    │  ├─ /api/compare (Revision delta)    │
                                    │  └─ /api/audit_logs                  │
                                    │                                      │
                                    │  ChromaDB ─── SentenceTransformers   │
                                    │  SQLite   ─── Audit & Entity store   │
                                    └──────────────────────────────────────┘
    """, language="text")

# ════════════════════════════════════════════════════════════════════════
# TAB 2 — UPLOAD & INGEST
# ════════════════════════════════════════════════════════════════════════
with tabs[1]:
    st.header("📄 Document Ingestion & Knowledge Indexing")
    st.write("Upload an AUTOSAR HLD PDF to extract text chunks, identify components, and build the vector index.")

    col_up, col_list = st.columns([2, 1])

    with col_up:
        uploaded_file = st.file_uploader("Select AUTOSAR HLD PDF", type=["pdf"])
        doc_version = st.text_input("Document Version", value="v1.0", help="Tag this revision (e.g. v1.0, v2.0)")

        if uploaded_file:
            if st.button("🚀 Process & Index Document", type="primary"):
                with st.spinner("Parsing PDF, building embeddings & storing in ChromaDB…"):
                    try:
                        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                        data = {"version": doc_version}
                        res = requests.post(f"{API_BASE_URL}/ingest", files=files, data=data, timeout=120)
                        if res.status_code == 200:
                            r = res.json()
                            st.success(f"✅ `{r['filename']}` processed successfully!")
                            c1, c2 = st.columns(2)
                            c1.metric("Text Chunks Indexed", r["indexed_chunks"])
                            c2.metric("Entities Extracted", r["extracted_entities_count"])
                        else:
                            st.error(f"Error: {res.text}")
                    except Exception as e:
                        st.error(f"Could not reach backend: {e}")

    with col_list:
        st.subheader("📚 Indexed Documents")
        try:
            res = requests.get(f"{API_BASE_URL}/documents", timeout=10)
            if res.status_code == 200:
                docs = res.json()
                if docs:
                    df = pd.DataFrame(docs)[["filename", "version", "total_pages"]]
                    st.dataframe(df, use_container_width=True, hide_index=True)
                else:
                    st.info("No documents yet. Upload one on the left.")
        except Exception:
            st.warning("Cannot fetch document list — backend offline?")

# ════════════════════════════════════════════════════════════════════════
# TAB 3 — GROUNDED Q&A
# ════════════════════════════════════════════════════════════════════════
with tabs[2]:
    st.header("🔍 Grounded Architecture Q&A")
    st.write("Ask any question about the uploaded design documents — answers come with exact page & section citations.")

    default_q = "What are the main software components and their interface ports?"
    query = st.text_input("Your Question", value=default_q)
    top_k = st.slider("Max source citations (Top-K)", 1, 8, 4)

    if st.button("🔍 Search", type="primary"):
        if not query.strip():
            st.warning("Please enter a question.")
        else:
            with st.spinner("Retrieving & synthesising evidence…"):
                try:
                    res = requests.post(
                        f"{API_BASE_URL}/query",
                        json={"query": query, "top_k": top_k},
                        timeout=60
                    )
                    if res.status_code == 200:
                        data = res.json()
                        st.markdown("### 💡 Answer")
                        st.markdown(data["answer"])

                        st.markdown(f"---\n### 📍 Source Citations ({len(data['citations'])} found)")
                        for i, c in enumerate(data["citations"]):
                            with st.expander(
                                f"**Citation {i+1}** — {c['source_doc']} | Page {c['page']} | "
                                f"Section: *{c['section']}* | Relevance: {c['relevance_score']*100:.0f}%"
                            ):
                                st.write(c["excerpt"])
                    else:
                        st.error(f"Query error: {res.text}")
                except Exception as e:
                    st.error(f"Backend error: {e}")

# ════════════════════════════════════════════════════════════════════════
# TAB 4 — COMPONENT INVENTORY
# ════════════════════════════════════════════════════════════════════════
with tabs[3]:
    st.header("🧩 AUTOSAR Entity Inventory & Review")
    st.write("Auto-extracted software components, interfaces, ports and signals from uploaded specifications.")

    try:
        res = requests.get(f"{API_BASE_URL}/entities", timeout=10)
        if res.status_code == 200:
            entities = res.json()
            if entities:
                df_e = pd.DataFrame(entities)

                # Summary metrics
                c1, c2, c3, c4 = st.columns(4)
                for col, etype in zip([c1, c2, c3, c4], ["SoftwareComponent", "Interface", "Port", "Signal"]):
                    count = len(df_e[df_e["entity_type"] == etype])
                    col.metric(etype, count)

                st.markdown("---")

                # Filter
                types = ["All"] + sorted(df_e["entity_type"].unique().tolist())
                sel = st.selectbox("Filter by type", types)
                filtered = df_e if sel == "All" else df_e[df_e["entity_type"] == sel]
                st.dataframe(
                    filtered[["id", "document_name", "entity_type", "entity_name", "source_page", "review_status"]],
                    use_container_width=True, hide_index=True
                )

                st.markdown("---")
                st.subheader("Engineer Review Decision")
                col_id, col_dec, col_btn = st.columns([1, 1, 1])
                with col_id:
                    eid = st.number_input("Entity ID", min_value=1, step=1, value=int(df_e["id"].iloc[0]))
                with col_dec:
                    decision = st.selectbox("Decision", ["approved", "rejected", "pending_review"])
                with col_btn:
                    st.write("")
                    st.write("")
                    if st.button("✅ Submit"):
                        r2 = requests.post(
                            f"{API_BASE_URL}/entity/review",
                            json={"entity_id": int(eid), "status": decision},
                            timeout=10
                        )
                        if r2.status_code == 200:
                            st.success(f"Entity {eid} marked as **{decision}**!")
                            st.rerun()
            else:
                st.info("No entities found. Upload a PDF first.")
    except Exception as e:
        st.warning(f"Error: {e}")

# ════════════════════════════════════════════════════════════════════════
# TAB 5 — REVISION COMPARE
# ════════════════════════════════════════════════════════════════════════
with tabs[4]:
    st.header("🔄 HLD Revision Comparison")
    st.write("Select two documents to detect added, removed, or changed architectural components between versions.")

    try:
        res_docs = requests.get(f"{API_BASE_URL}/documents", timeout=10)
        if res_docs.status_code == 200:
            doc_list = [d["filename"] for d in res_docs.json()]
            if len(doc_list) >= 2:
                col_a, col_b = st.columns(2)
                with col_a:
                    d1 = st.selectbox("📄 Baseline (older)", doc_list, index=0)
                with col_b:
                    d2 = st.selectbox("📄 New Revision", doc_list, index=1)

                if st.button("⚡ Compare Revisions", type="primary"):
                    res_cmp = requests.post(
                        f"{API_BASE_URL}/compare",
                        json={"doc1_name": d1, "doc2_name": d2},
                        timeout=30
                    )
                    if res_cmp.status_code == 200:
                        cmp = res_cmp.json()
                        s = cmp["summary"]

                        c1, c2, c3, c4 = st.columns(4)
                        c1.metric("Baseline Entities", s["total_doc1_entities"])
                        c2.metric("New Rev Entities",  s["total_doc2_entities"])
                        c3.metric("Added",   s["added_count"],   delta=f"+{s['added_count']}")
                        c4.metric("Removed", s["removed_count"], delta=f"-{s['removed_count']}", delta_color="inverse")

                        if cmp["inconsistencies"]:
                            st.markdown("---")
                            st.subheader(f"🔍 {len(cmp['inconsistencies'])} Differences Found")
                            df_cmp = pd.DataFrame(cmp["inconsistencies"])
                            st.dataframe(df_cmp, use_container_width=True, hide_index=True)
                        else:
                            st.success("✅ No architectural inconsistencies detected between the two versions.")
            else:
                st.info("Please upload at least 2 different PDF documents to compare.")
    except Exception as e:
        st.warning(f"Error: {e}")

# ════════════════════════════════════════════════════════════════════════
# TAB 6 — AUDIT LOG
# ════════════════════════════════════════════════════════════════════════
with tabs[5]:
    st.header("📜 Audit Trail & Governance Log")
    st.write("Every query, ingestion, comparison and engineer decision is logged here for traceability.")

    try:
        res_a = requests.get(f"{API_BASE_URL}/audit_logs", timeout=10)
        if res_a.status_code == 200:
            logs = res_a.json()
            if logs:
                df_l = pd.DataFrame(logs)
                st.dataframe(
                    df_l[["id", "timestamp", "action", "query_text", "confidence_score"]],
                    use_container_width=True, hide_index=True
                )
                st.caption(f"Showing last {len(logs)} entries.")
            else:
                st.info("No audit entries yet. Start uploading documents or asking questions.")
    except Exception as e:
        st.warning(f"Error: {e}")
