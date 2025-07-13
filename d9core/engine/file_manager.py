import json
import os
import shutil
from importlib.resources import files
from pathlib import Path

SYSTEM_DOCS = files("d9core.data") / "documents.json"
USER_DIR   = Path(os.environ.get("XDG_DATA_HOME", Path.home()/".local"/"share")) / "d9core"
USER_DOCS  = USER_DIR / "documents.json"

def ensure_user_docs(reset:bool = False) -> None:
    USER_DIR.mkdir(parents=True, exist_ok=True)
    if not USER_DOCS.exists() or reset:
        with SYSTEM_DOCS.open("rb") as src, USER_DOCS.open("wb") as dst:
            shutil.copyfileobj(src, dst)

ensure_user_docs(reset=True)

def get_documents() -> list[dict]:
    with USER_DOCS.open("r") as file:
        data = json.load(file)

    return data

def get_column(data: list[dict],column: str = 'id') -> list:
    return [i[column] for i in data]

def save_documents(data: list[dict]) -> None:
    with USER_DOCS.open("w") as file:
        json.dump(data, file, indent=2)

def update_status(data: list[dict], id: str, status: str = "read") -> None:
    for document in data:
        if document["id"] == id:
            document["status"] = status
            break

def update_action(data: list[dict], id: str, action: str = "read") -> None:
    for document in data:
        if document["id"] == id:
            document["action"] = action
            break

def update_notes(data: list[dict], id: str, notes: str = "read") -> None:
    for document in data:
        if document["id"] == id:
            document["notes"] = notes
            break

def get_entry(data: list[dict], id:str) -> dict:
    for document in data:
        if document["id"] == id:
            return document
        
    return {}