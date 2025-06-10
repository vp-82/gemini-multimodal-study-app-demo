# Multimodal Study Buddy

## Overview

The Multimodal Study Buddy is a web application that helps users generate study
guides from YouTube video lectures and PDF documents. Users can input a YouTube
URL and upload a PDF, and the application will use a multimodal AI model
(Google's Gemini) to synthesize information from both sources and produce a
comprehensive study guide in Markdown format.

## Prerequisites

- Python 3.8 or higher
- Pip (Python package installer)
- Google Cloud Project with the Vertex AI API enabled
- `gcloud` CLI authenticated with your Google Cloud account

## Environment Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_name>
    ```

2.  **Create a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    # On Windows, use: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    Create a `.env` file in the root directory of the project and add the following variables:
    ```env
    GOOGLE_PROJECT_ID="your-google-cloud-project-id"
    GOOGLE_LOCATION="your-google-cloud-region" # e.g., us-central1
    ```
    Replace `"your-google-cloud-project-id"` and `"your-google-cloud-region"`
    with your actual Google Cloud project ID and location/region. The location
    should be one where Vertex AI and the Gemini models are available.

## Running the Application

1.  **Ensure your virtual environment is activated:**
    ```bash
    source venv/bin/activate
    ```

2.  **Run the Flask application:**
    ```bash
    python app.py
    ```

3.  Open your web browser and navigate to `http://127.0.0.1:5000/`.

## How It Works

The application uses Flask as its web framework. When a user submits a YouTube URL and a PDF file:
1.  The backend receives the inputs.
2.  The `ai_services.multimodal_handler` module prepares the data and sends it
    to the Gemini multimodal model via the Vertex AI API.
3.  The AI model processes the video content (from the URL) and the PDF
    document.
4.  It generates a study guide in Markdown.
5.  The Flask app converts the Markdown to HTML and displays it on the results
    page.

## Key Files

-   `app.py`: Main Flask application file, handles routing and request
    processing.
-   `config.py`: Loads configuration settings, including Google Cloud project
    details.
-   `ai_services/multimodal_handler.py`: Contains the logic for interacting
    with the Gemini AI model.
-   `templates/`: HTML templates for the web interface.
    -   `index.html`: The main page with the input form.
    -   `results.html`: The page that displays the generated study guide.
-   `static/`: Static files (CSS).
    -   `css/style.css`: Stylesheet for the application.
-   `requirements.txt`: Lists Python dependencies.
-   `.env`: (To be created by user) Stores environment variables.
-   `README.md`: This file.

## Dependencies

The main dependencies are listed in `requirements.txt` and include:
-   Flask
-   google-generativeai
-   google-cloud-aiplatform
-   python-dotenv
-   Markdown

Install them using `pip install -r requirements.txt`.
