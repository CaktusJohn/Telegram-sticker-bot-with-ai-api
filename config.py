# config.py
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()

# Telegram / admin
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

# Facemint
FACEMINT_API_KEY = os.getenv("FACEMINT_API_KEY", "")

# Temp files
TMP_DIR = os.getenv("TMP_DIR", "tmp")
Path(TMP_DIR).mkdir(parents=True, exist_ok=True)

# Upload limits
try:
    MAX_PHOTO_MB = int(os.getenv("MAX_PHOTO_MB", "10"))
except ValueError:
    MAX_PHOTO_MB = 10

# Debug
DEBUG = os.getenv("DEBUG", "False").lower() in ("1", "true", "yes")

# Public host for media files
PUBLIC_HOST = os.getenv("PUBLIC_HOST", "localhost")
