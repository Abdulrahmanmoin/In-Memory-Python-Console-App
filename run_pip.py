import subprocess
import os

with open("pip_output.txt", "w") as f:
    process = subprocess.Popen(
        [r"backend\.venv\Scripts\python.exe", "-m", "pip", "install", "asyncpg==0.29.0"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        shell=True
    )
    for line in process.stdout:
        f.write(line)
        f.flush()
    process.wait()
