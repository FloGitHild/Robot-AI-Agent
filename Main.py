import json
import time
import sys
import settings

from agent_call import call_llm
from agent_tools import tool_registry, execute_actions
from Task_Manager import get_next_task
from agent_Memory import load_memory
from agent_vision import create_vision_data
from agent_start_stop import *

TASK_FILE = "tasks.json"
running = True




def main_loop():

    global running

    # =========================
    # START SYSTEM
    # =========================
    start_ollama()
    print("🤖 Robot Agent started")

    try:
        while running:

            # =========================
            # 1. VISION
            # =========================
            vision_raw = create_vision_data()

            try:
                vision = json.loads(vision_raw) if vision_raw else {}
            except Exception as e:
                print("⚠️ Vision parse error:", e)
                vision = {}

            # =========================
            # 2. TASK SYSTEM
            # =========================
            task = get_next_task(TASK_FILE)

            # =========================
            # 3. MEMORY
            # =========================
            memory = load_memory() if load_memory else []
            memory = memory[-10:]

            # =========================
            # 4. BUILD INPUT
            # =========================
            input_data = {
                "vision": vision,
                "task": task,
                "memory": memory
            }

            prompt = json.dumps(input_data, indent=2)

            # =========================
            # 5. LLM CALL
            # =========================
            raw_response = call_llm(prompt)

            # DEBUG (EXTREM WICHTIG)
            print("\n🧪 RAW LLM OUTPUT:\n", raw_response)

            if not raw_response or raw_response.strip() == "":
                print("⚠️ Empty LLM response")
                continue

            # =========================
            # 6. PARSE JSON
            # =========================
            try:
                response = json.loads(raw_response)
            except Exception as e:
                print("❌ JSON parse error:", e)
                print("RAW:", raw_response)
                continue

            # =========================
            # 7. EXECUTE TOOLS
            # =========================
            execute_actions(response, tool_registry)

            # =========================
            # 8. HEARTBEAT
            # =========================
            time.sleep(settings.CURRENT_HEARTBEAT)

    except KeyboardInterrupt:
        print("\n🧠 Ctrl+C detected -> stopping agent")
        running = False

    finally:
        stop_ollama()
        print("✅ Clean shutdown complete")
        sys.exit(0)


if __name__ == "__main__":
    main_loop()