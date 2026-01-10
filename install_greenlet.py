import subprocess
import sys
import os

def install_greenlet():
    venv_python = os.path.abspath("backend/.venv/Scripts/python.exe")
    print(f"Installing greenlet using {venv_python}...")
    try:
        result = subprocess.run(
            [venv_python, "-m", "pip", "install", "greenlet"],
            capture_output=True,
            text=True,
            check=True
        )
        print("Output:", result.stdout)
        print("Success!")
    except subprocess.CalledProcessError as e:
        print("Error:", e.stderr)
        sys.exit(1)

if __name__ == "__main__":
    install_greenlet()
