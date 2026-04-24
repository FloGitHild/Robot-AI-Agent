local_llm_model = "phi3" # "phi3", "gpt-4o", "mistral"
KNOWN_FACES_DIR = "face_database"
OBJECT_DETECTION_MODEL = "yolov8n.pt" # leichtes Modell, (n,s,m,l,x)
CURRENT_HEARTBEAT = 2 # Sekunden zwischen den Scans, wird angepasst je nach modus
CURRENT_MODE = "AUTO" # AUTO, PLAY, ASSIST, EXPLORE, IDLE