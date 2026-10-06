import os
import chromadb
from typing import List, Dict, Any, Tuple
from app.config import CHROMA_DIR, DEFAULT_COLLECTION_NAME

try:
    from sentence_transformers import SentenceTransformer
    HAS_ST = True
except Exception:
    HAS_ST = False

if not HAS_ST:
    from sklearn.feature_extraction.text import TfidfVectorizer
    import numpy as np

class RAGEngine:
    def __init__(self):
        self.chroma_client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        self.collection = self.chroma_client.get_or_create_collection(
            name=DEFAULT_COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}
        )
        if HAS_ST:
            self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
            self.mode = "sentence_transformer"
        else:
            self.tfidf = TfidfVectorizer(stop_words='english')
            self.mode = "tfidf_fallback"
            self._vocab_fitted = False

    def _get_embedding(self, text: str, corpus: List[str] = None) -> List[float]:
        if self.mode == "sentence_transformer":
            return self.embedding_model.encode(text).tolist()
        else:
            if corpus and not self._vocab_fitted:
                self.tfidf.fit(corpus + [text])
                self._vocab_fitted = True
            elif not self._vocab_fitted:
                self.tfidf.fit([text, "AUTOSAR HLD ECU software component interface signal"])
                self._vocab_fitted = True
            vec = self.tfidf.transform([text]).toarray()[0]
            norm = np.linalg.norm(vec)
            if norm > 0:
                vec = vec / norm
            return vec.tolist()

    def index_document_chunks(self, chunks: List[Dict[str, Any]], doc_filename: str) -> int:
        ids, documents, metadatas, embeddings = [], [], [], []
        all_texts = [c["text"] for c in chunks]

        for idx, chunk in enumerate(chunks):
            chunk_id = f"{doc_filename}_{chunk['metadata']['chunk_id']}_{idx}"
            text = chunk["text"]
            meta = {**chunk["metadata"], "filename": doc_filename}
            emb = self._get_embedding(text, corpus=all_texts)
            ids.append(chunk_id)
            documents.append(text)
            metadatas.append(meta)
            embeddings.append(emb)

        if ids:
            self.collection.add(ids=ids, documents=documents, metadatas=metadatas, embeddings=embeddings)
        return len(ids)

    def query(self, query_text: str, top_k: int = 4) -> Tuple[str, List[Dict], float]:
        query_emb = self._get_embedding(query_text)
        results = self.collection.query(query_embeddings=[query_emb], n_results=top_k)

        retrieved_texts = results["documents"][0] if results["documents"] else []
        metadatas      = results["metadatas"][0]  if results["metadatas"]  else []
        distances      = results["distances"][0]  if results["distances"]  else []

        if not retrieved_texts:
            return "No matching architecture evidence found in uploaded HLD documents.", [], 0.0

        citations, total_score = [], 0.0
        for doc_text, meta, dist in zip(retrieved_texts, metadatas, distances):
            similarity = max(0.0, 1.0 - dist)
            total_score += similarity
            citations.append({
                "source_doc": meta.get("filename", "Unknown"),
                "page": meta.get("page", 1),
                "section": meta.get("section", "General"),
                "relevance_score": round(similarity, 4),
                "excerpt": doc_text[:200] + "..." if len(doc_text) > 200 else doc_text
            })

        avg_conf = round(total_score / len(retrieved_texts), 2)
        answer = "Based on the AUTOSAR High-Level Design (HLD) specifications:\n\n"
        for c in citations:
            answer += f"- **{c['source_doc']} (Page {c['page']}, {c['section']})**: {c['excerpt']}\n"
        answer += f"\n**Confidence Score:** {avg_conf * 100:.1f}%\n"
        answer += f"**Grounded Verification:** {len(citations)} source citations retrieved."
        return answer, citations, avg_conf

rag_engine = RAGEngine()
