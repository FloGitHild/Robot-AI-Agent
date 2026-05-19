import json
import cv2
import face_recognition
import numpy as np
from ultralytics import YOLO
import pytesseract
from deepface import DeepFace
import os
import settings

yolo_model = YOLO(settings.OBJECT_DETECTION_MODEL)


# =========================
# FRAME
# =========================
def pick_frame():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    return frame if ret else None


# =========================
# FACES
# =========================
def face_recognition_and_emotion(frame, known_encodings, known_names):
    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb)
    face_encodings = face_recognition.face_encodings(rgb, face_locations)

    faces = []

    for (top, right, bottom, left), encoding in zip(face_locations, face_encodings):

        name = "unknown"
        confidence = 0.0

        if known_encodings:
            distances = face_recognition.face_distance(known_encodings, encoding)
            best = np.argmin(distances)

            if distances[best] < 0.5:
                name = known_names[best]
                confidence = float(1 - distances[best])

        center_x = ((left + right) / 2) / w
        center_y = ((top + bottom) / 2) / h
        width = (right - left) / w
        height = (bottom - top) / h

        emotion = "unknown"
        try:
            crop = frame[top:bottom, left:right]
            result = DeepFace.analyze(crop, actions=["emotion"], enforce_detection=False)
            emotion = result[0]["dominant_emotion"]
        except:
            pass

        faces.append({
            "name": name,
            "pos": {
                "x": round(center_x, 3),
                "y": round(center_y, 3),
                "w": round(width, 3),
                "h": round(height, 3)
            },
            "emotion": emotion,
            "confidence": round(confidence, 2)
        })

    return faces

def load_known_faces():
    encodings = []
    names = []

    if not os.path.exists(settings.KNOWN_FACES_DIR):
        print("[WARN] Known faces directory not found")
        return encodings, names

    for person in os.listdir(settings.KNOWN_FACES_DIR):
        person_path = os.path.join(settings.KNOWN_FACES_DIR, person)

        # ===== Folder structure (recommended) =====
        if os.path.isdir(person_path):
            for file in os.listdir(person_path):
                path = os.path.join(person_path, file)

                try:
                    img = face_recognition.load_image_file(path)
                    enc = face_recognition.face_encodings(img)

                    if enc:
                        encodings.append(enc[0])
                        names.append(person)

                except Exception as e:
                    print(f"[WARN] Failed to load {path}: {e}")

        # ===== Legacy single-file structure =====
        else:
            try:
                img = face_recognition.load_image_file(person_path)
                enc = face_recognition.face_encodings(img)

                if enc:
                    encodings.append(enc[0])
                    names.append(person.split(".")[0])

            except Exception as e:
                print(f"[WARN] Failed to load {person_path}: {e}")

    print("[INFO] Faces loaded:", sorted(set(names)))
    return encodings, names



# =========================
# OBJECTS
# =========================
def object_detection(frame):
    h, w, _ = frame.shape
    results = yolo_model(frame)

    objects = []

    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            label = yolo_model.names[cls]

            x1, y1, x2, y2 = box.xyxy[0].tolist()

            center_x = ((x1 + x2) / 2) / w
            center_y = ((y1 + y2) / 2) / h

            objects.append({
                "label": label,
                "pos": {
                    "x": round(center_x, 3),
                    "y": round(center_y, 3)
                },
                "confidence": round(float(box.conf[0]), 2)
            })

    return objects


# =========================
# OCR (clean)
# =========================
def ocr(frame):
    try:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]
        return pytesseract.image_to_string(gray).strip()
    except:
        return ""


# =========================
# MAIN OUTPUT (🔥 ONLY THIS GOES TO LLM)
# =========================
def create_vision_data():

    frame = pick_frame()
    if frame is None:
        return None

    known_encodings, known_names = load_known_faces()

    faces = face_recognition_and_emotion(frame, known_encodings, known_names)
    objects = object_detection(frame)
    text = ocr(frame)

    vision = {
        "faces": [
            {
                "name": f["name"],
                "pos": f["pos"],
                "emotion": f["emotion"]
            }
            for f in faces
        ],
        "objects": [
            {
                "label": o["label"],
                "pos": o["pos"]
            }
            for o in objects
        ],
        "text": text
    }

    return json.dumps(vision, indent=2)