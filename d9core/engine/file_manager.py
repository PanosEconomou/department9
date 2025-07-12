import json

DOCUMENT_PATH = 'data/documents.json'

def get_documents() -> dict:
    with open(DOCUMENT_PATH, 'r') as file:
        data = json.load(file)

    return data

def get_column(data: dict,column: str = 'id'):
    return [i[column] for i in data]