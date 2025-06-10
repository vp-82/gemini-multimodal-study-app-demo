"""
This module handles interactions with the Google Gemini AI model
to generate study guides based on YouTube videos and PDF documents.
This module handles interactions with the Google Gemini AI model
to generate study guides based on YouTube videos and PDF documents.
It includes functions for uploading files to Gemini and generating content
using a multimodal approach.
"""

from google import genai
from google.genai.types import (
    Part,
    SafetySetting,
    HarmCategory,
    HarmBlockThreshold,
    GenerateContentConfig,
)
import config
import logging

logger = logging.getLogger(__name__)

try:
    logger.info("Initializing Google GenAI Client for Vertex AI...")
    gcp_client = genai.Client(
        vertexai=True, project=config.PROJECT_ID, location=config.LOCATION
    )
    logger.info("Successfully initialized Google GenAI Client.")
except Exception as e:
    logger.error(f"Error initializing Google GenAI Client for Vertex AI: {e}")
    # Handle client initialization failure (e.g., exit, log critical error)
    # For a Flask app, this might be done once when the app starts.
    gcp_client = None


def generate_study_guide(youtube_url, pdf_file_storage):
    """
    Generates a study guide by interacting with the Gemini AI model.

    This function takes a YouTube URL and a PDF file, sends them to the
    Gemini model, and returns a study guide in Markdown format.

    Args:
        youtube_url (str): The URL of the YouTube video.
        pdf_file_storage (FileStorage): The PDF file object from Flask request.

    Returns:
        str: The generated study guide in Markdown format, or an error message
             if generation fails.
    """
    logger.info(
        f"generate_study_guide called with YouTube URL: {youtube_url} and PDF: {pdf_file_storage.filename}"
    )
    if not gcp_client:
        logger.error("AI service client not initialized.")
        return (
            "# An Error Occurred\n"
            "Sorry, the AI service client is not initialized. "
            "Please check server logs."
        )

    try:
        # Prepare the PDF part for the multimodal prompt
        pdf_bytes = pdf_file_storage.read()
        pdf_part = Part.from_bytes(data=pdf_bytes, mime_type="application/pdf")

        video_part = Part.from_uri(file_uri=youtube_url, mime_type="video/mp4")

        logger.info("Preparing prompt parts...")
        # Construct the prompt parts, including instructions and file data
        prompt_parts = [
            "You are an expert academic assistant.",
            "Please analyze the content of the provided YouTube video lecture "
            "and the attached PDF document.",
            "Create a comprehensive, well-structured study guide in Markdown "
            "format that synthesizes the key concepts, definitions, and "
            "examples from both sources.",
            "Your guide should have a clear structure with headings and bullet "
            "points.",
            "Please analyze the content of the provided YouTube video lecture "
            "and the attached PDF document.",
            "Create a comprehensive, well-structured study guide in Markdown "
            "format that synthesizes the key concepts, definitions, and "
            "examples from both sources.",
            "Your guide should have a clear structure with headings and bullet "
            "points.",
            "Here is the PDF document:",
            pdf_part,
            "And here is the video:",
            video_part,
        ]

        # Configure generation parameters, including safety settings.
        # These settings are permissive; adjust as needed for content
        # filtering.
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
                threshold=HarmBlockThreshold.BLOCK_NONE,  # type: ignore
            ),
        ]
        generation_config = GenerateContentConfig(safety_settings=safety_settings)
        # Configure generation parameters, including safety settings.
        # These settings are permissive; adjust as needed for content
        # filtering.
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
                threshold=HarmBlockThreshold.BLOCK_NONE,  # type: ignore
            ),
        ]
        generation_config = GenerateContentConfig(safety_settings=safety_settings)

        # Call the Gemini model to generate content.
        # Call the Gemini model to generate content.
        # Uses the specified model ID from config and sends the prompt parts
        # and generation configuration.
        logger.info(f"Calling Gemini model ({config.MODEL_ID}) to generate content...")
        response = gcp_client.models.generate_content(
            model=config.MODEL_ID,
            contents=prompt_parts,
            config=generation_config,
        )
        logger.info("Successfully received response from Gemini model.")

        return response.text

    except Exception as e:
        logger.error(f"Error generating study guide: {e}")
        # Return a user-friendly error message in Markdown format
        error_message = (
            "# An Error Occurred\n\n"
            "Sorry, there was a problem generating the study guide. "
            "Please check the console for more details.\n\n"
            f"**Error:**\n`{e}`"
        )
        return error_message
        error_message = (
            "# An Error Occurred\n\n"
            "Sorry, there was a problem generating the study guide. "
            "Please check the console for more details.\n\n"
            f"**Error:**\n`{e}`"
        )
        return error_message
