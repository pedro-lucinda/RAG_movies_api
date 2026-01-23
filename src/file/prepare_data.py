from src.infra.db.chromadb import collection
from src.file.read_csv import get_data_from_csv
import json

def prepare_data_for_upsert(file_path: str) -> dict[str, list[str]]:
    data = get_data_from_csv("src/data/data.csv")

    data_to_upsert = {
      "ids": [],
      "documents": []
    }
    for item in data:
        data_to_upsert["ids"].append(item["Position"])
        data_to_upsert["documents"].append(json.dumps(item))

    return data_to_upsert

