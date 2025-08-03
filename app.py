"""
Main Gradio application file for the Multimodal Study Buddy.
"""
import logging
import gradio as gr
from ai_services.multimodal_handler import generate_study_guide

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def create_study_guide(youtube_url, pdf_file):
    """
    The main function called by the Gradio interface to generate the study guide.

    Args:
        youtube_url (str): The URL of the YouTube video.
        pdf_file (file): A file-like object for the uploaded PDF.

    Returns:
        str: The generated study guide in Markdown format.
    """
    if not youtube_url or not pdf_file:
        return "Error: Please provide both a YouTube URL and a PDF file."

    logging.info(f"Generating guide for URL: {youtube_url} and PDF: {pdf_file.name}")

    try:
        # Read the content of the uploaded file
        with open(pdf_file.name, "rb") as f:
            pdf_content = f.read()

        # Call the AI handler
        markdown_guide, _ = generate_study_guide(
            youtube_url, pdf_content, pdf_file.name
        )
        return markdown_guide
    except Exception as e:
        logging.error(f"An error occurred: {e}", exc_info=True)
        return f"An unexpected error occurred. Please check the logs. Error: {e}"

# --- Gradio Interface Definition ---
with gr.Blocks() as demo:
    gr.Markdown("# Multimodal Study Buddy")
    gr.Markdown("Provide a YouTube link and a PDF chapter to generate a consolidated study guide.")

    with gr.Row():
        youtube_url_input = gr.Textbox(label="YouTube Video URL")
        pdf_file_input = gr.File(label="PDF File", file_types=[".pdf"])

    generate_button = gr.Button("Generate Guide")

    output_guide = gr.Markdown(label="Your AI-Generated Study Guide")

    generate_button.click(
        fn=create_study_guide,
        inputs=[youtube_url_input, pdf_file_input],
        outputs=output_guide,
    )

if __name__ == "__main__":
    demo.launch()