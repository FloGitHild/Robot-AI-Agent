import subprocess
import os

PIPER = "/home/florian/Daten/Florian/Freizeit/Robot-AI-Agent/piper/piper"

MODEL = "models/de_DE-kerstin-low.onnx"
CONFIG = "models/de_DE-kerstin-low.onnx.json"
out_file = "/home/florian/Daten/Florian/Freizeit/Robot-AI-Agent/robot_voice.wav"


def TTS_Say(text, speed=0.8):

    cmd = [
        PIPER,
        "-m", MODEL,
        "-c", CONFIG,
        "-f", out_file,
        "--length_scale", str(speed)
    ]

    result = subprocess.run(cmd, input=text.encode("utf-8"), capture_output=True, timeout=30)

    if result.returncode != 0:
        print(result.stderr.decode())
        return

    if not os.path.exists(out_file):
        print("Keine Datei erzeugt")
        return

    subprocess.run(["aplay", out_file])

