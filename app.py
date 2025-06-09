from flask import Flask, render_template, request

import config
import markdown  # Import the new library

# Import our AI handler function
from ai_services.multimodal_handler import generate_study_guide

# Initialize Flask app
app = Flask(__name__)


# Route for the main page
@app.route("/", methods=["GET", "POST"])
def index():
    # Handle POST request when form is submitted
    if request.method == "POST":
        youtube_url = request.form.get("youtube_url")
        pdf_file = request.files.get("pdf_file")

        # Validate inputs
        if not pdf_file or pdf_file.filename == "":
            return "Error: No PDF file selected.", 400
        if not youtube_url:
            return "Error: No YouTube URL provided.", 400

        # Generate study guide using AI handler
        generated_markdown = generate_study_guide(youtube_url, pdf_file)

        # Convert markdown to HTML
        generated_html = markdown.markdown(generated_markdown)

        # Render results page with generated HTML
        return render_template("results.html", content_html=generated_html)

    # Render main page for GET request
    return render_template("index.html")


# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
