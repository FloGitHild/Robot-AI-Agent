import json
import requests

url = "http://localhost:11434/api/chat"

with open("request.json", "r", encoding="utf-8") as f:
    data = json.load(f)

response = requests.post(url, json=data)
result = response.json()

print(result["message"]["content"])