import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

DB_CONFIG = {
  "dbname": os.getenv("DB_DATABASE"),
  "user": os.getenv("DB_USERNAME"),
  "password": os.getenv("DB_PASSWORD"),
  "host": os.getenv("DB_HOST"),
  "port": os.getenv("DB_PORT")
}

print(DB_CONFIG)