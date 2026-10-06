import os
from pathlib import Path

# When running on Render, use /data (persistent disk mount)
# When running locally, use the project root /data folder
IS_RENDER = os.environ.get("RENDER", False)

if IS_RENDER:
    DATA_DIR = Path("/data")
else:
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    DATA_DIR = BASE_DIR / "data"

UPLOAD_DIR = DATA_DIR / "uploads"
CHROMA_DIR = DATA_DIR / "chroma_db"
DB_PATH = DATA_DIR / "autosar_platform.db"

# Create directories if not exist
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
CHROMA_DIR.mkdir(parents=True, exist_ok=True)

# Embedding settings
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
DEFAULT_COLLECTION_NAME = "autosar_hld_knowledge"
