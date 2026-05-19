from datetime import datetime, timedelta
import os
import time
from urllib import response
import Task_Manager
import agent_call
import agent_tools
import agent_vision
import create_JSON
import settings
TODO_FILE = "ToDo.txt"

# Ensure file exists
if not os.path.exists(TODO_FILE):
    with open(TODO_FILE, "w"):
        pass


# Continuous monitoring loop
while True:
    task_list = Task_Manager.scan_tasks(TODO_FILE)

    for task in task_list:
        task_id, scheduled_time,type, name, description, priority = task
        print(f"Type: {type} | Task: {name} | Description: {description} | Priority: {priority}")
        

        # Inputs:
        # mode: PLAY, ASSIST, EXPLORE, AUTO, IDLE
        # vision: current vision input (can be empty)
        # task: current task description
        # message: user input (can be empty)

        settings.CURRENT_MODE = "AUTO" # This can be set based on the task or other conditions
        #generate promt based on task and execute it
        
        # first call of the LLM to get the tools to execute, then execute the tools and call the LLM again to get the final answer
        message = "no user input"
        create_JSON.create_json(settings.CURRENT_MODE, agent_vision.create_vision_data(), task, message, datetime.now());
        llm_result = agent_call()
        tool_results = agent_tools(llm_result)

        #prepare final prompt with tool results and call LLM again to get final answer
        create_JSON.create_json(settings.CURRENT_MODE, agent_vision.create_vision_data(), task, tool_results, datetime.now());
        llm_result = agent_call()
        # Delete executed task
        Task_Manager.delete_task(TODO_FILE, task_id)
    # Scan interval
    time.sleep(settings.CURRENT_HEARTBEAT)