import json
import settings
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
import requests
import os
from Task_Manager import *

TASK_FILE = "tasks.json"


#===================================
#       Tool Wrapper
#===================================

def create_task(type, name, description, priority, time=None):
    if not time:
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return add_task(
        file=TASK_FILE,
        time_str=time,
        type=type,
        name=name,
        description=description,
        priority=priority
    )

def scan_tasks_tool():
    return scan_tasks(TASK_FILE)

def delete_task_tool(id):
    return delete_task(TASK_FILE, id)

def change_task_priority_tool(id, priority):
    return change_priority(TASK_FILE, id, priority)

def web_search(query, max_results=5):
    results = []

    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results):
            results.append({
                "title": r["title"],
                "link": r["href"],
                "snippet": r["body"]
            })

    if not results:
        return {"error": "no results"}

    try:
        r = requests.get(results[0]["link"], timeout=5)
        soup = BeautifulSoup(r.text, "html.parser")

        text = soup.get_text()
        return {
            "query": query,
            "top_result": results[0],
            "content": text[:2000]
        }

    except:
        return {
            "query": query,
            "error": "failed to load page"
        }

def weather(location):
    load_dotenv()

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": location,
        "appid": os.getenv("Openweather_Key"),
        "units": "metric",
        "lang": "de"
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        return {
            "city": location,
            "temp": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "description": data["weather"][0]["description"]
        }

    except:
        return {
            "city": location,
            "error": "weather fetch failed"
        }


def movement(dir, speed):
    speed = max(0, min(100, int(speed)))

    actions = {
        "forward": f"Moving forward at speed {speed}",
        "backward": f"Moving backward at speed {speed}",
        "left": f"Turning left at speed {speed}",
        "right": f"Turning right at speed {speed}"
    }

    result = actions.get(dir, "Unknown direction")

    print(result)

    return {
        "direction": dir,
        "speed": speed,
        "status": result
    }

def append_gallery(time, comment):
    entry = {
        "time": time,
        "comment": comment
    }

    print(f"Gallery updated: {entry}")

    return {
        "status": "saved",
        "entry": entry
    }


tool_registry = {
    "web_search": web_search,
    "weather": weather,
    "movement": movement,
    "append_gallery": append_gallery,

    # TASK SYSTEM
    "create_task": add_task,
    "scan_tasks": scan_tasks,
    "delete_task": delete_task,
    "change_task_priority": change_priority
}




def execute_actions(response, tool_registry):
    results = []

    if not isinstance(response, dict):
        return {"error": "invalid response format"}

    message = response.get("message", "")
    actions = response.get("actions", [])

    # Message loggen
    if message:
        print("🤖:", message)
        add_memory("message", message)

    if not isinstance(actions, list):
        actions = [actions]

    for action in actions:
        tool_name = action.get("tool")
        args = action.get("args", {})

        if tool_name not in tool_registry:
            continue

        try:
            print(f"🔧 Tool: {tool_name}")

            result = tool_registry[tool_name](**args)

            results.append({
                "tool": tool_name,
                "args": args,
                "result": result
            })

            # Memory speichern
            add_memory("tool", {
                "tool": tool_name,
                "args": args,
                "result": result
            })

        except Exception as e:
            results.append({
                "tool": tool_name,
                "error": str(e)
            })

    return {
        "message": message,
        "tool_results": results
    }