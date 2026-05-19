# Main Programm, manages the Call of agents, LLM, and TTS / STT
import time
import TTS
import Tasks
import sys

if __name__ == '__main__':
    try:
        while True:
            print("\nGet Current Tasks\n")
            Current_Tasks = Tasks.Task_Trigger()
            if Current_Tasks != None:
                for i in Current_Tasks:
                    print(str(i) + "\n")
                    TTS.TTS_Say(f"Aufgabe '{i['name']}' wurde erstellt mit Zeitstempel {i['created']} mit dem Typ {i['type']} und Kathegorie {i['category']}. Ziel Zeit ist {i['target_time']}. Die Beschreibung ist '{i['description']}', und priorität {i['priority']}.")
                    print("schlafen für 60 sek.\n\n\n")
            time.sleep(60)
            
            
    except KeyboardInterrupt:
        print("Interrupted")
        sys.exit(0)
