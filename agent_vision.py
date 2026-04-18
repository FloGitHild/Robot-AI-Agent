import json
from pydoc import text
import cv2
import face_recognition
import numpy as np
from ultralytics import YOLO
import pytesseract
from deepface import DeepFace
import os
import settings


# =========================
# LOAD KNOWN FACES
# =========================
def load_known_faces():
    known_encodings = []
    known_names = []

    for filename in os.listdir(settings.KNOWN_FACES_DIR):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            img = face_recognition.load_image_file(os.path.join(settings.KNOWN_FACES_DIR, filename))
            enc = face_recognition.face_encodings(img)

            if enc:
                known_encodings.append(enc[0])
                known_names.append(filename.split(".")[0])
                
    print("[INFO] Faces geladen:", known_names)
    return known_encodings, known_names

# =========================
# CAPTURE IMAGE
# =========================
def pick_frame():
    cap = cv2.VideoCapture(0)

    ret, frame = cap.read()

    if not ret or frame is None:
        print("Kamera nicht verfügbar")
        return None

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return frame

# =========================
# FACE DETECTION + RECOGNITION
# =========================
def face_recognition_and_emotion(frame, known_encodings, known_names):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb)
    face_encodings = face_recognition.face_encodings(rgb, face_locations)

    faces = []

    for (top, right, bottom, left), encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_encodings, encoding)
        name = "Unknown"

        if True in matches:
            idx = matches.index(True)
            name = known_names[idx]

        # Emotion (optional)
        emotion = "unknown"
        try:
            face_img = frame[top:bottom, left:right]
            result = DeepFace.analyze(face_img, actions=['emotion'], enforce_detection=False)
            emotion = result[0]['dominant_emotion']
        except:
            pass

        faces.append({
            "name": name,
            "position": (left, top, right, bottom),
            "emotion": emotion
        })

# =========================
# OBJECT DETECTION
# =========================
def object_detection(frame):
    results = YOLO(settings.OBJECT_DETECTION_MODEL)(frame)

    objects = []
    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            label = YOLO(settings.OBJECT_DETECTION_MODEL).names[cls]
            objects.append(label)

    return objects

# =========================
# OCR (TEXT RECOGNITION)
# =========================
def ocr(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)




def create_vision_json():
    #frame holen
    frame = pick_frame()
    #gesichterdatenbank & namen laden
    known_encodings, known_names = load_known_faces()
    #gesichter & emotion erkennen
    faces = face_recognition_and_emotion(frame, known_encodings, known_names)
    # objekte erkennen
    objects = object_detection(frame)
    # text erkennen
    text = ocr(frame)

    

    # =========================
    # OUTPUT
    # =========================
    print("\n--- RESULT ---")

    print("\n👤 Faces:")
    for f in faces:
        print(f)

    print("\n📦 Objects:")
    print(objects)

    print("\n📝 Text:")
    print(text.strip())

    # Optional: anzeigen
    cv2.imshow("Frame", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



create_vision_json()