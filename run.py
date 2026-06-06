import os
import subprocess
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def run_train():
    print("🤖 Training model...")
    subprocess.run([sys.executable, os.path.join(BASE_DIR, "ml_model", "train_model.py")])


def run_app():
    print("🌐 Starting web app...")
    subprocess.run([sys.executable, os.path.join(BASE_DIR, "web_app", "app.py")])


if __name__ == "__main__":
    run_train()
    run_app()