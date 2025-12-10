# utils.py
import os
import json
import zipfile
from datetime import datetime
from typing import Any

ROOT_DIR = os.getcwd()
DATA_DIR = os.path.join(ROOT_DIR, "data")
BACKUP_DIR = os.path.join(DATA_DIR, "backups")
NOTES_FILE = os.path.join(DATA_DIR, "notes.json")
CALC_LOG = os.path.join(DATA_DIR, "calculator_log.csv")

def ensure_dirs():
    """Ensure data directories and minimal files exist."""
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(BACKUP_DIR, exist_ok=True)
    if not os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)
    if not os.path.exists(CALC_LOG):
        open(CALC_LOG, "a").close()

def now_str() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def read_json(path: str, default: Any = None):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default

def write_json(path: str, data: Any):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def read_text(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""

def write_text(path: str, text: str):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

def make_backup(prefix: str = "pps_backup") -> str:
    """Create a zip backup of the data folder (excluding backups folder)."""
    ensure_dirs()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_name = f"{prefix}_{timestamp}.zip"
    zip_path = os.path.join(BACKUP_DIR, zip_name)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(DATA_DIR):
            # Skip backing up the backups folder itself
            if os.path.abspath(BACKUP_DIR).startswith(os.path.abspath(root)):
                continue
            for file in files:
                full = os.path.join(root, file)
                arc = os.path.relpath(full, DATA_DIR)
                zf.write(full, arc)
    return zip_path

def list_backups():
    ensure_dirs()
    files = [f for f in os.listdir(BACKUP_DIR) if f.endswith(".zip")]
    files.sort(reverse=True)
    return files

def restore_backup(filename: str) -> bool:
    path = os.path.join(BACKUP_DIR, filename)
    if not os.path.exists(path):
        return False
    with zipfile.ZipFile(path, "r") as zf:
        zf.extractall(DATA_DIR)
    return True
