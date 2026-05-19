# Main Programm, manages the Call of agents, LLM, and TTS / STT
import time
import TTS
import Tasks
import sys

if __name__ == '__main__':
    try:
        while True:
            print("\nAktuelle Tasks Abfragen\n")
            Current_Tasks,Future_Tasks = Tasks.Task_Trigger()

            if Current_Tasks != None:
                print("\nAktuelle AUfgaben: ")
                for i in Current_Tasks:
                    print(i)
                    TTS.TTS_Say(f"Aufgabe '{i['name']}' wurde erstellt mit Zeitstempel {i['created']} mit dem Typ {i['type']} und Kathegorie {i['category']}. Ziel Zeit ist {i['target_time']}. Die Beschreibung ist '{i['description']}', und priorität {i['priority']}.")
                    

            if Future_Tasks != None:
                print("\nZukünfltige Aufgaben:")
                for i in Future_Tasks:
                    print(i)

            print("schlafen für 60 sek.\n\n\n")
            time.sleep(60)
            
            
    except KeyboardInterrupt:
        print("Interrupted")
        sys.exit(0)
