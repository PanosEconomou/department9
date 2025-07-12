import json
from importlib.resources import files

DOCUMENT_PATH = files("d9core.data") / "documents.json"

def get_documents() -> dict:
    with DOCUMENT_PATH.open("r") as file:
        data = json.load(file)

    return data

def get_column(data: dict,column: str = 'id'):
    return [i[column] for i in data]