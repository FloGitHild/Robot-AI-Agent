import json
import os
import uuid
from datetime import datetime

TASK_FILE = "tasks.json"


# -----------------------------
# LOAD / SAVE
# -----------------------------
def load_tasks():
    if not os.path.exists(TASK_FILE):
        return {"tasks": []}

    with open(TASK_FILE, "r") as f:
        return json.load(f)


def save_tasks(data):
    with open(TASK_FILE, "w") as f:
        json.dump(data, f, indent=4)



# -----------------------------
# CREATE TASK (SAFE)
# -----------------------------
def create_task(
    name,
    description,
    task_type="User",
    category="None",
    target_time=None,
    priority=1,
    parent_goal_name=""
):

    data = load_tasks()

    task = {
        "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "target_time": target_time,
        "type": task_type,
        "category": category,
        "name": name,
        "description": description,
        "priority": priority,
        "parent_goal_name": parent_goal_name
    }

    data.append(task)
    save_tasks(data)

    return task["parent_goal_name"]


# -----------------------------
# LIST TASKS (SORTED)
# -----------------------------
def list_tasks():
    data = load_tasks()

    def sort_key(t):
        target = t["target_time"] if t["target_time"] else "9999-99-99 99:99:99"
        return (target, -t["priority"], t["created"])

    tasks = sorted(data, key=sort_key)

    return tasks

# -----------------------------
# PRIORITY UPDATE
# -----------------------------
def change_priority(task_id, new_priority):
    data = load_tasks()

    for t in data["tasks"]:
        if t["id"] == task_id:
            t["priority"] = new_priority
            save_tasks(data)
            return True

    return False


# -----------------------------
# DELETE TASK
# -----------------------------
def delete_task(name):
    data = load_tasks()

    new_tasks = [t for t in data["tasks"] if t["name"] != name]

    if len(new_tasks) == len(data["tasks"]):
        return False

    data["tasks"] = new_tasks
    save_tasks(data)
    return True


def Task_Trigger():
    data = load_tasks()
    urgent_tasks = []
    for i in data:
        Task_Tartget_Time = datetime.strptime(i["target_time"], '%Y-%m-%d %H:%M:%S')
        if datetime.now() >= Task_Tartget_Time:
            urgent_tasks.append(i)
    
    return urgent_tasks