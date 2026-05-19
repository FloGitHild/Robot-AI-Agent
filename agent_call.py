import json
import requests
import re


url = "http://localhost:11434/api/chat"


def call_llm(prompt):
    data = {
        "model": "phi3",
        "messages": [
            {
                "role": "system",
                "content": "You are a robot agent. ALWAYS respond with valid JSON ONLY. No markdown. No explanation."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "stream": False
    }

    try:
        response = requests.post(url, json=data)
        result = response.json()

        print("DEBUG FULL RESPONSE:", result)

        content = result.get("message", {}).get("content", None)

        print("DEBUG CONTENT:", content)

        parsed = extract_json(content)

        if parsed is None:
            print("❌ Could not parse JSON")
            return None

        return parsed

    except Exception as e:
        print("❌ LLM call failed:", e)
        return None




def extract_json(text):
    if not text:
        return None

    # remove code fences
    text = text.replace("```json", "").replace("```", "")

    # remove backticks
    text = text.replace("`", "")

    # keep only first JSON object
    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        return None

    text = text[start:end+1]

    try:
        return json.loads(text)
    except Exception as e:
        print("JSON parse failed:", e)
        return None