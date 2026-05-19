import subprocess
import time
import requests
import signal
import sys

ollama_process = None
running = True

def start_ollama():
    global ollama_process
    print("🚀 Starting Ollama...")

    ollama_process = subprocess.Popen(
        ["ollama", "serve"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    time.sleep(2)  # give API time to boot


def stop_ollama():
    global ollama_process

    if ollama_process:
        print("🛑 Stopping Ollama...")

        ollama_process.terminate()

        try:
            ollama_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            ollama_process.kill()

        ollama_process = None