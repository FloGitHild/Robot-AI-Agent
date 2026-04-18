import json
import cv2
import face_recognition
import numpy as np
from ultralytics import YOLO
import pytesseract
from deepface import DeepFace
import os
import settings

# =========================
# GLOBAL MODEL (WICHTIG!)
# =========================
yolo_model = YOLO(settings.OBJECT_DETECTION_MODEL)

# =========================
# LOAD KNOWN FACES (MULTI-IMAGE SUPPORT)
# =========================
def load_known_faces():
    encodings = []
    names = []

    for person in os.listdir(settings.KNOWN_FACES_DIR):
        person_path = os.path.join(settings.KNOWN_FACES_DIR, person)

        if os.path.isdir(person_path):
            for file in os.listdir(person_path):
                path = os.path.join(person_path, file)

                img = face_recognition.load_image_file(path)
                enc = face_recognition.face_encodings(img)

                if enc:
                    encodings.append(enc[0])
                    names.append(person)
        else:
            # fallback für alte Struktur
            img = face_recognition.load_image_file(person_path)
            enc = face_recognition.face_encodings(img)

            if enc:
                encodings.append(enc[0])
                names.append(person.split(".")[0])

    print("[INFO] Faces geladen:", list(set(names)))
    return encodings, names


# =========================
# CAPTURE IMAGE
# =========================
def pick_frame():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()

    if not ret or frame is None:
        print("Kamera nicht verfügbar")
        return None

    return frame  # NICHT direkt RGB machen!


# =========================
# FACE DETECTION + BEST MATCH
# =========================
def face_recognition_and_emotion(frame, known_encodings, known_names):
    import numpy as np
    import cv2
    import face_recognition
    from deepface import DeepFace

    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb)
    face_encodings = face_recognition.face_encodings(rgb, face_locations)

    faces = []

    for (top, right, bottom, left), encoding in zip(face_locations, face_encodings):

        # =========================
        # BEST MATCH (statt compare_faces)
        # =========================
        name = "Unknown"
        confidence = 0.0

        if len(known_encodings) > 0:
            distances = face_recognition.face_distance(known_encodings, encoding)
            best_idx = np.argmin(distances)

            if distances[best_idx] < 0.5:
                name = known_names[best_idx]
                confidence = float(1 - distances[best_idx])

        # =========================
        # NORMALISIERTE POSITION (0–1)
        # =========================
        center_x = ((left + right) / 2) / w
        center_y = ((top + bottom) / 2) / h
        width = (right - left) / w
        height = (bottom - top) / h

        # =========================
        # EMOTION (optional)
        # =========================
        emotion = "unknown"
        try:
            face_img = frame[top:bottom, left:right]
            result = DeepFace.analyze(face_img, actions=['emotion'], enforce_detection=False)
            emotion = result[0]['dominant_emotion']
        except:
            pass

        # =========================
        # OUTPUT
        # =========================
        faces.append({
            "name": name,
            "confidence": round(confidence, 2),
            "position": {
                "center_x": round(center_x, 3),
                "center_y": round(center_y, 3),
                "width": round(width, 3),
                "height": round(height, 3)
            },
            "emotion": emotion
        })

    return faces


# =========================
# OBJECT DETECTION (OPTIMIERT)
# =========================
def object_detection(frame):
    h, w, _ = frame.shape

    results = yolo_model(frame)

    objects = []

    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            label = yolo_model.names[cls]

            # Bounding Box (Pixel)
            x1, y1, x2, y2 = box.xyxy[0].tolist()

            # =========================
            # NORMALISIERUNG (0–1)
            # =========================
            center_x = ((x1 + x2) / 2) / w
            center_y = ((y1 + y2) / 2) / h
            width = (x2 - x1) / w
            height = (y2 - y1) / h

            confidence = float(box.conf[0])

            objects.append({
                "label": label,
                "confidence": round(confidence, 2),
                "position": {
                    "center_x": round(center_x, 3),
                    "center_y": round(center_y, 3),
                    "width": round(width, 3),
                    "height": round(height, 3)
                }
            })

    return objects


# =========================
# OCR
# =========================
def ocr(frame):
    try:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]

        text = pytesseract.image_to_string(gray)
        return text.strip() if text else ""

    except Exception as e:
        print("OCR Fehler:", e)
        return ""


# =========================
# SAVE NEW FACE (MIT CROP!)
# =========================
def save_new_face(frame, name):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    faces = face_recognition.face_locations(rgb)

    if len(faces) == 0:
        print("Kein Gesicht erkannt")
        return False

    top, right, bottom, left = faces[0]
    face_img = frame[top:bottom, left:right]

    folder = os.path.join(settings.KNOWN_FACES_DIR, name)
    os.makedirs(folder, exist_ok=True)

    count = len(os.listdir(folder))
    filename = os.path.join(folder, f"{count}.jpg")

    cv2.imwrite(filename, face_img)
    print(f"[INFO] Gesicht gespeichert: {filename}")

    return True


# =========================
# MAIN
# =========================
def create_vision_data():
    frame = pick_frame()
    if frame is None:
        return None

    known_encodings, known_names = load_known_faces()

    faces = face_recognition_and_emotion(frame, known_encodings, known_names)
    objects = object_detection(frame)
    text = ocr(frame)

    print("\n--- RESULT ---")

    print("\n👤 Faces:")
    for f in (faces or []):
        print(f)

        if f["name"] == "Unknown":
            new_name = input("Neues Gesicht erkannt (Name eingeben oder Enter): ")
            if new_name:
                save_new_face(frame, new_name)
                print(f"Gesicht '{new_name}' hinzugefügt.")

    print("\n📦 Objects:")
    print(objects)

    print("\n📝 Text:")
    print(text)

    vision_data = {
        "faces": faces or [],
        "objects": objects or [],
        "text": text or ""
    }

    return json.dumps(vision_data, indent=4)

# =========================
# RUN
# =========================
if __name__ == "__main__":
    print(create_vision_data())