import json


def load_data(filepath: str):
    with open(filepath, mode="r", encoding="utf-8") as f:
        data = json.load(f)
    return data
