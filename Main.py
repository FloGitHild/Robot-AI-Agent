# Main Programm, manages the Call of agents, LLM, and TTS / STT
import time
import TTS
import Tasks
import sys

# Source - https://stackoverflow.com/q/21120947
# Posted by Dan, modified by community. See post 'Timeline' for change history
# Retrieved 2026-05-19, License - CC BY-SA 3.0

if __name__ == '__main__':
    try:
        while True:
            Current_Tasks = Tasks.Task_Trigger()
            if Current_Tasks != None:
                for i in Current_Tasks:
                    print(i)
                    TTS.TTS_Say(f"Aufgabe '{i['name']}' wurde erstellt mit Zeitstempel {i['created']} mit dem Typ {i['type']} und Kathegorie {i['category']}. Ziel Zeit ist {i['target_time']}. Die Beschreibung ist '{i['description']}', und priorität {i['priority']}.")

            
            
    except KeyboardInterrupt:
        print("Interrupted")
        sys.exit(0)
