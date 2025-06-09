"""
This module handles interactions with the Google Gemini AI model to generate
study guides based on YouTube videos and PDF documents.
It includes functions for uploading files to Gemini and generating content
using a multimodal approach.
"""
from google.cloud import aiplatform
import vertexai
from vertexai.generative_models import (
    GenerativeModel,
    Part,
    SafetySetting,
    HarmCategory,
    HarmBlockThreshold,
    GenerationConfig,
)
import config
import os


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
    # print("AI Handler: Firing up the model with the correct Vertex AI client...") # Debug print

    try:
        # Initialize Vertex AI
        aiplatform.init(project=config.PROJECT_ID, location=config.LOCATION)

        # Instantiate the generative model
        model = GenerativeModel(config.MODEL_ID)

        # Prepare the PDF part for the multimodal prompt
        # print(f"AI Handler: Reading PDF content for '{pdf_file_storage.filename}'...") # Debug print
        pdf_bytes = pdf_file_storage.read()
        pdf_part = Part.from_data(data=pdf_bytes, mime_type="application/pdf") # Corrected Part creation

        # Prepare the video part for the multimodal prompt from the YouTube URL
        # print(f"AI Handler: Creating video part for URL: {youtube_url}...") # Debug print
        video_part = Part.from_uri(uri=youtube_url, mime_type="video/mp4") # Updated Part creation, parameter name is 'uri'

        # Construct the prompt parts, including instructions and file data
        prompt_parts = [
            "You are an expert academic assistant.",
            "Please analyze the content of the provided YouTube video lecture and the attached PDF document.",
            "Create a comprehensive, well-structured study guide in Markdown format that synthesizes the key concepts, definitions, and examples from both sources.",
            "Your guide should have a clear structure with headings and bullet points.",
            "Here is the PDF document:",
            pdf_part,
            "And here is the video:",
            video_part,
        ]

        # Configure generation parameters, including safety settings
        # These settings are permissive; adjust as needed for content filtering.
        generation_config = GenerationConfig( # Changed from GenerateContentConfig
            safety_settings=[
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
        )

        # Call the Gemini model to generate content
        # Uses the specified model ID from config and sends the prompt parts
        # and generation configuration.
        # print(
        #     f"AI Handler: Calling the Gemini model ({config.MODEL_ID}) via direct generate_content..." # Debug print
        # )

        response = model.generate_content( # Changed client.models.generate_content to model.generate_content
            contents=prompt_parts,  # The multimodal content for the prompt
            generation_config=generation_config,  # Configuration for generation and safety
        )

        # print("AI Handler: Successfully received response from Gemini.") # Debug print

        # Return the text part of the model's response
        return response.text

    except Exception as e:
        # print(f"AI Handler: An error occurred: {e}") # Debug print for server log
        # Return a user-friendly error message in Markdown format
        return f"# An Error Occurred\n\nSorry, there was a problem generating the study guide. Please check the console for more details.\n\n**Error:**\n`{e}`"
