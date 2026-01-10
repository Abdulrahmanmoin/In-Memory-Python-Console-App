import asyncio
import os
import sys
from pathlib import Path

# Add Windows-specific event loop fix for psycopg
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Add the project root and backend folder to sys.path
root = Path(__file__).resolve().parent
backend_path = root / "backend"
src_path = backend_path / "src"
sys.path.append(str(root))
sys.path.append(str(backend_path))
sys.path.append(str(src_path))

from sqlmodel import SQLModel
from backend.src.database.connection import async_engine
from backend.src.models.user import User
from backend.src.models.task import Task

async def init_db():
    log_file = "db_init_log.txt"
    with open(log_file, "w") as f:
        f.write("Starting initialization...\n")
        try:
            async with async_engine.begin() as conn:
                f.write("Creating tables...\n")
                await conn.run_sync(SQLModel.metadata.create_all)
            f.write("Database initialized successfully!\n")
        except Exception as e:
            f.write(f"Error initializing database: {e}\n")
    
    print("Done. Check db_init_log.txt")

if __name__ == "__main__":
    asyncio.run(init_db())
