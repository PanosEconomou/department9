import requests
import json
import time
import os
from importlib.resources import files
from pathlib import Path

MODEL = "hermes3"
SYSTEM_DOCS = files("d9core.data") / "documents.json"
USER_DIR   = Path(os.environ.get("XDG_DATA_HOME", Path.home()/".local"/"share")) / "d9core"
USER_DOCS  = USER_DIR / "documents.json"

def chat_with_npc(user_input, history):
    return