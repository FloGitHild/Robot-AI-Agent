import json
import os
from datetime import datetime

MEMORY_FILE = "memory.json"


def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return []

    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except:
            return []


def save_memory(memory):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=4)


def add_memory(entry_type, content):
    memory = load_memory()

    memory.append({
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type": entry_type,
        "content": content
    })

    save_memory(memory)