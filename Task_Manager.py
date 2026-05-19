import json
import uuid
from datetime import datetime
import os

def add_task(file, time_str, type, name, description, priority):
    task = {
        "id": str(uuid.uuid4()),
        "time": time_str,
        "type": type,
        "name": name,
        "description": description,
        "priority": int(priority)
    }

    # Datei laden
    if os.path.exists(file):
        with open(file, "r", encoding="utf-8") as f:
            try:
                tasks = json.load(f)
            except:
                tasks = []
    else:
        tasks = []

    tasks.append(task)

    # speichern
    with open(file, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=4)

    return task["id"]


def scan_tasks(file):
    if not os.path.exists(file):
        return []

    with open(file, "r", encoding="utf-8") as f:
        try:
            tasks = json.load(f)
        except:
            return []

    now = datetime.now()
    valid_tasks = []

    for t in tasks:
        try:
            task_time = datetime.strptime(t["time"], "%Y-%m-%d %H:%M:%S")

            if task_time <= now:
                valid_tasks.append(t)
        except:
            continue

    # SORTIERUNG:
    # 1. priority (1 = highest)
    # 2. time (older first)
    valid_tasks.sort(key=lambda x: (x["priority"], x["time"]))

    return valid_tasks


def delete_task(file, task_id):
    if not os.path.exists(file):
        return False

    with open(file, "r", encoding="utf-8") as f:
        try:
            tasks = json.load(f)
        except:
            return False

    tasks = [t for t in tasks if t["id"] != task_id]

    with open(file, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=4)

    return True

def change_priority(file, task_id, new_priority):
    if not os.path.exists(file):
        return False

    with open(file, "r", encoding="utf-8") as f:
        try:
            tasks = json.load(f)
        except:
            return False

    for t in tasks:
        if t["id"] == task_id:

            # nur Agent Tasks dürfen geändert werden
            if t["type"] != "Agent":
                return False

            t["priority"] = int(new_priority)
            break

    with open(file, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=4)

    return True


def get_next_task(file):
    tasks = scan_tasks(file)

    if not tasks:
        return None

    return tasks[0]