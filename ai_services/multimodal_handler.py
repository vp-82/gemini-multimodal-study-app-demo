"""Handles interactions with the Google Gemini AI model.

This module provides functions to generate study guides by sending multimodal
(video and PDF) content to the Google Gemini model via the Vertex AI API.
"""
import logging

from google import genai
from google.genai.types import (
    GenerateContentConfig,
    HarmBlockThreshold,
    HarmCategory,
    Part,
    SafetySetting,
)

import config

logger = logging.getLogger(__name__)

try:
    logger.info("Initializing Google GenAI Client for Vertex AI...")
    gcp_client = genai.Client(
        vertexai=True, project=config.PROJECT_ID, location=config.LOCATION
    )
    logger.info("Successfully initialized Google GenAI Client.")
except Exception as e:
    logger.error(f"Error initializing Google GenAI Client for Vertex AI: {e}")
    gcp_client = None


def generate_study_guide(youtube_url, pdf_file_storage):
    """Generates a study guide from a YouTube video and a PDF file.

    This function interacts with the Gemini AI model, sending it a YouTube URL
    and a PDF file. It then returns a study guide in Markdown format.

    Args:
        youtube_url (str): The URL of the YouTube video.
        pdf_file_storage (FileStorage): The PDF file object from the Flask
            request.

    Returns:
        str: The generated study guide in Markdown format, or a user-friendly
             error message if generation fails.
    """
    logger.info(
        "generate_study_guide called with YouTube URL: %s and PDF: %s",
        youtube_url,
        pdf_file_storage.filename,
    )
    if not gcp_client:
        logger.error("AI service client not initialized.")
        return (
            "# An Error Occurred\n"  # Corrected newline escaping
            "Sorry, the AI service client is not initialized. "
            "Please check server logs."
        )

    try:
        pdf_bytes = pdf_file_storage.read()
        pdf_part = Part.from_bytes(data=pdf_bytes, mime_type="application/pdf")
        video_part = Part.from_uri(file_uri=youtube_url, mime_type="video/mp4")

        logger.info("Preparing prompt parts...")

        # Load the system prompt from the dedicated text file
        with open("prompts/system_prompt.txt", "r") as f:
            system_prompt = f.read()

        prompt_parts = [
            system_prompt,
            "Here is the PDF document:",
            pdf_part,
            "And here is the video:",
            video_part,
        ]

        safety_settings = [
            SafetySetting(
                category=HarmCategory.HARM_CATEGORY_HARASSMENT,
                threshold=HarmBlockThreshold.BLOCK_NONE,
            ),
            SafetySetting(
                category=HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                threshold=HarmBlockThreshold.BLOCK_NONE,
            ),
            SafetySetting(
                category=HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                threshold=HarmBlockThreshold.BLOCK_NONE,
            ),
            SafetySetting(
                category=HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=HarmBlockThreshold.BLOCK_NONE,
            ),
        ]
        generation_config = GenerateContentConfig(safety_settings=safety_settings)

        logger.info("Calling Gemini model (%s) to generate content...", config.MODEL_ID)
        response = gcp_client.models.generate_content(
            model=config.MODEL_ID,
            contents=prompt_parts,
            config=generation_config,
        )
        logger.info("Successfully received response from Gemini model.")

        return response.text

    except Exception as e:
        logger.error("Error generating study guide: %s", e)
        error_message = (
            "# An Error Occurred\n\n"  # Corrected newline escaping
            "Sorry, there was a problem generating the study guide. "
            "Please check the console for more details.\n\n"
            f"**Error:**\n`{e}`"
        )
        return error_message
