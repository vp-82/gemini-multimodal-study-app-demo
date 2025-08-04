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


async def generate_study_guide(youtube_url, pdf_content, pdf_filename):
    """Generates a study guide from a YouTube video and PDF content.

    Args:
        youtube_url (str): The URL of the YouTube video.
        pdf_content (bytes): The content of the PDF file.
        pdf_filename (str): The original filename of the PDF.

    Returns:
        tuple[str, str]: A tuple containing the generated study guide and the
                         system prompt used.
    """
    logger.info(
        "Async generate_study_guide called with URL: %s and PDF: %s",
        youtube_url,
        pdf_filename,
    )
    if not gcp_client:
        logger.error("AI service client not initialized.")
        yield "# An Error Occurred\nSorry, the AI service client is not initialized."
        return

    try:
        pdf_part = Part.from_bytes(data=pdf_content, mime_type="application/pdf")
        video_part = Part.from_uri(file_uri=youtube_url, mime_type="video/mp4")

        logger.info("Preparing prompt parts...")

        # Load the system prompt from the dedicated text file
        with open("prompts/system_prompt.txt", "r") as f:
            system_prompt = f.read()

        contents = [
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

        logger.info("Calling async generate_content_stream...")

        # Use the async client and 'async for'
                response_stream = await gcp_client.aio.models.generate_content_stream(
            model=config.MODEL_ID,
            contents=contents,
            generation_config=generation_config,
        )

        async for chunk in response_stream:
            yield chunk.text

    except Exception as e:
        logger.error("Error in async generation: %s", e, exc_info=True)
        yield f"# An Error Occurred\n\nSorry, there was a problem: {e}"
