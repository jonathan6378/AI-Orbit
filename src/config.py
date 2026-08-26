import os
from pathlib import Path

from dotenv import load_dotenv


# Project root
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables
load_dotenv(BASE_DIR / ".env")


# Directories
DATA_DIR = BASE_DIR / "data"
LOG_DIR = BASE_DIR / "logs"


# Output files
ENTITIES_FILE = DATA_DIR / "entities.json"
RELATIONSHIPS_FILE = DATA_DIR / "relationships.json"


# API configuration
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")


# Pipeline configuration
TARGET_MIN_RECORDS = 250
TARGET_MAX_RECORDS = 300


# Make sure required directories exist
DATA_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)