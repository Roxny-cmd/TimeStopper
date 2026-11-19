from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATABASE_DIR = BASE_DIR / "database"

DB_PATH = DATABASE_DIR / "timestopper.db"

DATABASE_URL = f"sqlite:///{DB_PATH.as_posix()}"
