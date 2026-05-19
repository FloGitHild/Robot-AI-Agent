from datetime import datetime
import uuid

def add_task(file, time_str,type, name, description, priority):
    """
    Add a new task to the ToDo file with a UUID.
    """
    task_id = str(uuid.uuid4())
    entry = f"{task_id}#{time_str}#{type}#{name}#{description}#{priority}\n"
    with open(file, "a", encoding="utf-8") as f:
        f.write(entry)
    return task_id


def scan_tasks(file):
    """
    Read tasks from the file, return tasks ready to execute.
    Sorted by time, then by priority (highest first).
    """
    tasks = []
    now = datetime.now()

    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("#")
            if len(parts) != 6:
                continue  # ignore malformed old lines

            task_id, time_str, type, name, description, priority = parts
            task_time = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
            if task_time <= now:
                tasks.append((task_id, task_time,type, name, description, int(priority)))

    # Sort by time first, then by priority (descending)
    tasks.sort(key=lambda x: (x[1], -x[4]))
    return tasks


def delete_task(file, task_id_to_delete):
    """
    Delete a task by its UUID.
    """
    with open(file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = [line for line in lines if not line.startswith(task_id_to_delete)]

    with open(file, "w", encoding="utf-8") as f:
        f.writelines(new_lines)


def change_priority(file, task_ID):
    # hier funktion zum ändern der Prio
    print()