import json
import settings
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
import requests
import os


def select_tool(tools, task):
    # Einfache Heuristik: Wenn "search" im Task, dann Websuche, wenn "weather", dann Wetter, sonst Bewegung
    if "search" in task.lower():
        return "web_search"
    elif "weather" in task.lower():
        return "weather"
    elif any(dir in task.lower() for dir in ["forward", "backward", "left", "right"]):
        return "movement"
    elif "gallery" in task.lower():
        return "append_gallery"
    else:
        return None




def web_search(query, max_results=5):
    results = []

    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results):
            results.append({
                "title": r["title"],
                "link": r["href"],
                "snippet": r["body"]
            })

    try:
        r = requests.get(results[0]["link"], timeout=5)
        soup = BeautifulSoup(r.text, "html.parser")

        # einfacher Text
        text = soup.get_text()
        print(f"Web search results for '{query}': {text[:2000]}")
        return text[:2000]  # begrenzen!
    except:
        return "Fehler beim Laden"
    
def weather(location):
    load_dotenv()
    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": location,
        "appid": os.getenv("Openweather_Key"),
        "units": "metric",
        "lang": "de"
    }

    response = requests.get(url, params=params)
    data = response.json()

    return {
        "city": location,
        "temp": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "description": data["weather"][0]["description"]
    }


def movement(dir, speed):
    match dir:
        case "forward":
            print(f"Moving forward at speed {speed}")
        case "backward":
            print(f"Moving backward at speed {speed}")
        case "left":
            print(f"Turning left at speed {speed}")
        case "right":
            print(f"Turning right at speed {speed}")
        case _:
            print("Unknown direction")

def append_gallery(time, comment):
    print(f"Appending gallery at time {time} with comment: {comment}")

