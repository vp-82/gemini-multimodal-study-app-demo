import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Google Cloud Settings
PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID")
LOCATION = os.getenv("GOOGLE_LOCATION", "global")

# Gemini Model Settings
MODEL_ID = "gemini-2.5-pro-preview-06-05"
