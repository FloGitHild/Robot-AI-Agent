import json
import agent_vision
import settings

def create_json(mode, vision, task, message, time):
    with open("request.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

        # Bestimmen des Inhalts basierend auf dem Modus
        match mode:
            case "PLAY":
                role_content = "You are there to play with people and have fun."
                settings.CURRENT_HEARTBEAT = 0
            case "ASSIST":
                role_content = "You are a helpful assistant."
                settings.CURRENT_HEARTBEAT = 0
            case "EXPLORE":
                role_content = "You are a explorer."
                settings.CURRENT_HEARTBEAT = 0
            case "AUTO":
                role_content = "You are an autonomous agent."
                settings.CURRENT_HEARTBEAT = 0
            case "IDLE":
                role_content = "You can Interact with people, but dont make any plans or take any actions on your own."
                settings.CURRENT_HEARTBEAT = 0
            case _:
                return "Modus unbekannt"

        # Kontextinformationen für die Platzhalter
        context = {
            "llm_modell": settings.local_llm_model,
            "role_content": role_content,
            "message": message,
            "vision": vision,
            "task": task,
            "time": time
        }

        # Erstellen der JSON-Daten mit Platzhaltern
        data = {
            "model": "{llm_modell}",
            "messages": [
                {"role": "system", "content": "{role_content}"},
                {"role": "user", "content": "User input: {message}\nVision: {vision}\nTask: {task}\nTime: {time}\n"}
            ]
        }

        for msg in data["messages"]:
            for key, value in context.items():
                msg["content"] = msg["content"].replace(f"{{{key}}}", str(value))


    