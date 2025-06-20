import logging
from flask import Flask, render_template, request

import config
import markdown  # Import the new library

# Import our AI handler function
from ai_services.multimodal_handler import generate_study_guide

# Configure logging
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)


# Route for the main page
@app.route("/", methods=["GET", "POST"])
def index():
    # Handle POST request when form is submitted
    if request.method == "POST":
        logger.info("Received POST request to generate study guide")
        youtube_url = request.form.get("youtube_url")
        pdf_file = request.files.get("pdf_file")

        # Validate inputs
        if not pdf_file or pdf_file.filename == "":
            logger.error("Missing PDF file. Error: No PDF file selected.")
            return "Error: No PDF file selected.", 400
        if not youtube_url:
            logger.error("Missing YouTube URL. Error: No YouTube URL provided.")
            return "Error: No YouTube URL provided.", 400

        logger.info(f"YouTube URL: {youtube_url}, PDF File: {pdf_file.filename}")

        # Generate study guide using AI handler
        generated_markdown = generate_study_guide(youtube_url, pdf_file)

        # Convert markdown to HTML
        generated_html = markdown.markdown(generated_markdown)

        # Render results page with generated HTML
        logger.info("Successfully generated study guide and rendered results page")
        return render_template("results.html", content_html=generated_html)

    # Render main page for GET request
    logger.info("Received GET request for main page")
    return render_template("index.html")


# Run the Flask app
if __name__ == "__main__":
    logger.info("Application starting...")
    app.run(debug=True)
