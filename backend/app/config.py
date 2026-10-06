import os
from pathlib import Path

# Render free tier has no persistent disk, so use /tmp for demo
# (files reset on restart — fine for presentation/demo purposes)
IS_RENDER = os.environ.get("RENDER", "false").lower() == "true"

if IS_RENDER:
    DATA_DIR = Path("/tmp/autosar_data")
else:
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    DATA_DIR = BASE_DIR / "data"

UPLOAD_DIR = DATA_DIR / "uploads"
CHROMA_DIR = DATA_DIR / "chroma_db"
DB_PATH    = DATA_DIR / "autosar_platform.db"

# These dirs are always writable (/tmp on Render, local on dev)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
CHROMA_DIR.mkdir(parents=True, exist_ok=True)

# Embedding settings
EMBEDDING_MODEL_NAME   = "all-MiniLM-L6-v2"
DEFAULT_COLLECTION_NAME = "autosar_hld_knowledge"
