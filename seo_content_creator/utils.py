import json

def load_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_html(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def save_html(path: str, content: str):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)