import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Google Cloud Settings
# Project ID for Google Cloud services
PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID")
# Location for Google Cloud services, defaults to "global"
LOCATION = os.getenv("GOOGLE_LOCATION", "global")

# Gemini Model Settings
# Model ID for the Gemini API
MODEL_ID = "gemini-2.5-pro-preview-06-05"
