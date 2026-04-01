from datetime import datetime, timedelta
import os
import time
import Task_Manager

TODO_FILE = "ToDo.txt"

# Ensure file exists
if not os.path.exists(TODO_FILE):
    with open(TODO_FILE, "w"):
        pass

# Create example tasks
time_30 = (datetime.now() + timedelta(seconds=30)).strftime("%Y-%m-%d %H:%M:%S")
time_20 = (datetime.now() + timedelta(seconds=20)).strftime("%Y-%m-%d %H:%M:%S")
time_10 = (datetime.now() + timedelta(seconds=10)).strftime("%Y-%m-%d %H:%M:%S")

# Tasks scheduled for 30 seconds later
Task_Manager.add_task(TODO_FILE, time_30, "Task1", "This is the first task", 1)
Task_Manager.add_task(TODO_FILE, time_30, "Task2", "This is the second task", 2)
Task_Manager.add_task(TODO_FILE, time_30, "Task3", "This is the third task", 3)

# Tasks scheduled for 20 seconds later
Task_Manager.add_task(TODO_FILE, time_20, "Task4", "This is the fourth task", 5)
Task_Manager.add_task(TODO_FILE, time_20, "Task5", "This is the fifth task", 4)
Task_Manager.add_task(TODO_FILE, time_20, "Task6", "This is the sixth task", 1)
Task_Manager.add_task(TODO_FILE, time_20, "Task7", "This is the seventh task", 2)
Task_Manager.add_task(TODO_FILE, time_20, "Task8", "This is the eighth task", 6)
Task_Manager.add_task(TODO_FILE, time_20, "Task9", "This is the ninth task", 2)

# Tasks scheduled for 10 seconds later
Task_Manager.add_task(TODO_FILE, time_10, "Task10", "This is the tenth task", 5)
Task_Manager.add_task(TODO_FILE, time_10, "Task11", "This is the eleventh task", 3)
Task_Manager.add_task(TODO_FILE, time_10, "Task12", "This is the twelfth task", 4)
Task_Manager.add_task(TODO_FILE, time_10, "Task13", "This is the thirteenth task", 1)
Task_Manager.add_task(TODO_FILE, time_10, "Task14", "This is the fourteenth task", 2)
Task_Manager.add_task(TODO_FILE, time_10, "Task15", "This is the fifteenth task", 3)

# Continuous monitoring loop
while True:
    task_list = Task_Manager.scan_tasks(TODO_FILE)

    for task in task_list:
        task_id, scheduled_time, name, description, priority = task
        print(f"Task: {name} | Description: {description} | Priority: {priority}")

        # Delete executed task
        Task_Manager.delete_task(TODO_FILE, task_id)
    # Scan interval
    time.sleep(2)