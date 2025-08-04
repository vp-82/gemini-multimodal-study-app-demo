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

async def create_study_guide_stream(youtube_url, pdf_file):
    """
    An async generator function that streams the study guide generation process.

    Args:
        youtube_url (str): The URL of the YouTube video.
        pdf_file (file): A file-like object for the uploaded PDF.

    Yields:
        str: The accumulating study guide in Markdown format.
    """
    if not youtube_url or not pdf_file:
        yield "Error: Please provide both a YouTube URL and a PDF file."
        return

    yield "Processing inputs and preparing to generate... Please wait."

    logging.info(f"Streaming guide for URL: {youtube_url} and PDF: {pdf_file.name}")

    try:
        with open(pdf_file.name, "rb") as f:
            pdf_content = f.read()

        full_guide = ""
        # Use 'async for' to iterate over the async generator
        async for chunk in generate_study_guide(
            youtube_url, pdf_content, pdf_file.name
        ):
            full_guide += chunk
            yield full_guide

    except Exception as e:
        logging.error(f"An error occurred during streaming: {e}", exc_info=True)
        yield f"An unexpected error occurred. Please check the logs. Error: {e}"


# --- Gradio Interface Definition ---
with gr.Blocks() as demo:
    gr.Markdown("# Multimodal Study Buddy")
    gr.Markdown("Provide a YouTube link and a PDF chapter to generate a consolidated study guide.")

    with gr.Row():
        youtube_url_input = gr.Textbox(label="YouTube Video URL")
        pdf_file_input = gr.File(label="PDF File", file_types=[".pdf"])

    generate_button = gr.Button("Generate Guide")

    output_guide = gr.Markdown(label="Your AI-Generated Study Guide")

    # This event handles the streaming output
    generate_event = generate_button.click(
        fn=create_study_guide_stream,
        inputs=[youtube_url_input, pdf_file_input],
        outputs=output_guide,
    )

    # This event chain handles the button UI updates
    generate_event.then(
        lambda: gr.update(value="Generating...", interactive=False),
        outputs=generate_button,
    ).then(
        lambda: gr.update(value="Generate Guide", interactive=True),
        outputs=generate_button,
    )


if __name__ == "__main__":
    demo.launch()
