from google import genai
from google.genai.types import (
    HarmCategory,
    HarmBlockThreshold,
    Part,
    Blob,
    GenerateContentConfig,
    SafetySetting,
)
import config
import os


def upload_to_gemini(path, mime_type=None):
    """
    Uploads a file to Gemini's File API using the correct method.
    """
    # This is the correct top-level function to upload a file from a path.
    file = genai.upload_file(
        path=path, display_name=os.path.basename(path), mime_type=mime_type
    )
    print(f"Uploaded file '{file.display_name}' as: {file.uri}")
    return file


def generate_study_guide(youtube_url, pdf_file_storage):
    """
    This is the core function that interacts with the Gemini API using the
    correct client-based pattern for Vertex AI.
    """
    print("AI Handler: Firing up the model with the correct Vertex AI client...")

    try:
        # 1. Initialize the client for Vertex AI. This is correct.
        client = genai.Client(
            vertexai=True, project=config.PROJECT_ID, location=config.LOCATION
        )

        # 2. Prepare the multimodal parts for the prompt. This is correct.
        print(f"AI Handler: Reading PDF content for '{pdf_file_storage.filename}'...")
        pdf_bytes = pdf_file_storage.read()
        pdf_part = Part(inline_data=Blob(mime_type="application/pdf", data=pdf_bytes))

        print(f"AI Handler: Creating video part for URL: {youtube_url}...")
        video_part = Part.from_uri(file_uri=youtube_url, mime_type="video/mp4")

        # 3. Construct the prompt. This is correct.
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

        # 4. Create the generation configuration. This is correct.
        generation_config = GenerateContentConfig(
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

        # 5. Make a single, direct call to the API.
        # This is the corrected part. We no longer use get_model().
        print(
            f"AI Handler: Calling the Gemini model ({config.MODEL_ID}) via direct generate_content..."
        )

        response = client.models.generate_content(
            model=config.MODEL_ID,
            contents=prompt_parts,
            config=generation_config,
        )

        print("AI Handler: Successfully received response from Gemini.")

        # 6. Return the generated text.
        return response.text

    except Exception as e:
        print(f"AI Handler: An error occurred: {e}")
        return f"# An Error Occurred\n\nSorry, there was a problem generating the study guide. Please check the console for more details.\n\n**Error:**\n`{e}`"
