# Multimodal Study Buddy (Gradio Version)

## Overview

The Multimodal Study Buddy is a web application that helps users generate study
guides from YouTube video lectures and PDF documents. This version uses Gradio
to provide a simple and clean user interface. Users can input a YouTube
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
    python3 -m venv .venv
    source .venv/bin/activate
    # On Windows, use: .venv\Scripts\activate
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
    source .venv/bin/activate
    ```

2.  **Run the Gradio application:**
    ```bash
    python app.py
    ```

3.  Open your web browser and navigate to the local URL provided by Gradio (usually `http://127.0.0.1:7860`).

## How It Works

The application uses Gradio as its web framework. When a user submits a YouTube URL and a PDF file:
1.  The `create_study_guide` function is triggered.
2.  The function calls the `ai_services.multimodal_handler` module, which prepares the data and sends it
    to the Gemini multimodal model via the Vertex AI API.
3.  The AI model processes the video content (from the URL) and the PDF
    document.
4.  It generates a study guide in Markdown.
5.  Gradio renders the Markdown in the output component.

## Key Files

-   `app.py`: Main Gradio application file.
-   `config.py`: Loads configuration settings, including Google Cloud project
    details.
-   `ai_services/multimodal_handler.py`: Contains the logic for interacting
    with the Gemini AI model.
-   `requirements.txt`: Lists Python dependencies.
-   `.env`: (To be created by user) Stores environment variables.
-   `README.md`: This file.