from flask import Flask, render_template, request

import config

# --- Add these debug lines ---
print("--- DEBUGGING CONFIG ---")
print(f"Project ID loaded in config: {config.PROJECT_ID}")
print("------------------------")
import markdown  # Import the new library

# Import our AI handler function
from ai_services.multimodal_handler import generate_study_guide

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        youtube_url = request.form.get("youtube_url")
        pdf_file = request.files.get("pdf_file")

        if not pdf_file or pdf_file.filename == "":
            return "Error: No PDF file selected.", 400
        if not youtube_url:
            return "Error: No YouTube URL provided.", 400

        # Call the AI handler to get the markdown string
        generated_markdown = generate_study_guide(youtube_url, pdf_file)

        # Convert the markdown string to HTML right here
        generated_html = markdown.markdown(generated_markdown)

        # Pass the converted HTML to the template
        return render_template("results.html", content_html=generated_html)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
