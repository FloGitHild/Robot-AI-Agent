local_llm_model = "qwen3.5:latest" # "phi3:latest", "mistral:latest  ", "qwen3.5:latest"
KNOWN_FACES_DIR = "face_database"
OBJECT_DETECTION_MODEL = "yolov8n.pt" # leichtes Modell, (n,s,m,l,x)
CURRENT_HEARTBEAT = 2 # Sekunden zwischen den Scans, wird angepasst je nach modus
CURRENT_MODE = "AUTO" # AUTO, PLAY, ASSIST, EXPLORE, IDLE