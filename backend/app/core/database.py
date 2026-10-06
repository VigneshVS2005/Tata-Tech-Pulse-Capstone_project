import sqlite3
import json
from app.config import DB_PATH

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT UNIQUE NOT NULL,
            file_path TEXT NOT NULL,
            version TEXT,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            total_pages INTEGER,
            status TEXT DEFAULT 'processed'
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT NOT NULL,
            query_text TEXT,
            response_text TEXT,
            citations_json TEXT,
            confidence_score REAL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS extracted_entities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            document_name TEXT NOT NULL,
            entity_type TEXT NOT NULL,
            entity_name TEXT NOT NULL,
            description TEXT,
            source_page INTEGER,
            review_status TEXT DEFAULT 'pending_review'
        )
    ''')

    conn.commit()
    conn.close()

def log_audit_action(action, query_text="", response_text="", citations=None, confidence=0.95):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO audit_logs (action, query_text, response_text, citations_json, confidence_score)
        VALUES (?, ?, ?, ?, ?)
    ''', (action, query_text, response_text, json.dumps(citations or []), confidence))
    conn.commit()
    conn.close()

def register_document(filename, file_path, version="v1.0", total_pages=1):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO documents (filename, file_path, version, total_pages)
        VALUES (?, ?, ?, ?)
    ''', (filename, file_path, version, total_pages))
    conn.commit()
    conn.close()

def save_extracted_entity(doc_name, entity_type, entity_name, description="", page=1):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO extracted_entities (document_name, entity_type, entity_name, description, source_page)
        VALUES (?, ?, ?, ?, ?)
    ''', (doc_name, entity_type, entity_name, description, page))
    conn.commit()
    conn.close()

def get_all_documents():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM documents ORDER BY uploaded_at DESC')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_all_audit_logs():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM audit_logs ORDER BY timestamp DESC LIMIT 50')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_extracted_entities(doc_name=None):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    if doc_name:
        cursor.execute('SELECT * FROM extracted_entities WHERE document_name = ?', (doc_name,))
    else:
        cursor.execute('SELECT * FROM extracted_entities')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def update_entity_status(entity_id, status):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('UPDATE extracted_entities SET review_status = ? WHERE id = ?', (status, entity_id))
    conn.commit()
    conn.close()
