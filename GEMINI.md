# GEMINI.MD: AI Collaboration Guide

This document provides essential context for AI models interacting with this project. Adhering to these guidelines will ensure consistency and maintain code quality.

## 1. Project Overview & Purpose

* **Primary Goal:** A web application that generates study guides from YouTube video lectures and PDF documents using Google's Gemini multimodal AI model.
* **Business Domain:** EdTech / Educational Tools.

## 2. Core Technologies & Stack

* **Languages:** Python 3.8+
* **Frameworks & Runtimes:** Flask
* **Databases:** None. The application is stateless.
* **Key Libraries/Dependencies:**
    * `google-genai`: For interacting with the Gemini AI model.
    * `Flask`: Web framework.
    * `python-dotenv`: For managing environment variables.
    * `Markdown`: For converting generated Markdown to HTML.
* **Package Manager(s):** pip

## 3. Architectural Patterns

* **Overall Architecture:** Monolithic Application. The architecture is simple, with a single Flask application serving as the entry point and handling all requests. It follows a basic Model-View-Controller (MVC) pattern where:
    * **Model:** The AI interaction logic is separated into the `ai_services` module.
    * **View:** HTML templates are rendered by Flask.
    * **Controller:** The `app.py` file handles routing and business logic.
* **Directory Structure Philosophy:**
    * `/app.py`: Main Flask application and entry point.
    * `/config.py`: Configuration settings, primarily for the AI model and Google Cloud.
    * `/ai_services`: Contains the logic for interacting with the Gemini AI model.
    * `/templates`: Holds the HTML templates for the web interface.
    * `/static`: Contains static assets like CSS and JavaScript.
    * `/requirements.txt`: Lists all Python dependencies.

## 4. Coding Conventions & Style Guide

* **Formatting:** All Python code must adhere strictly to the **PEP 8** style guide. Use an autoformatter like `black` or `autopep8` to ensure consistency.
    * **Indentation:** 4 spaces.
    * **Line Length:** Keep lines under 88 characters where possible to improve readability.
* **Docstrings:** All modules, functions, and classes should have clear and concise docstrings following the Google Python Style Guide format.
* **Naming Conventions:**
    * `variables`, `functions`: `snake_case` (`my_variable`)
    * `files`: `snake_case` (`multimodal_handler.py`)
* **API Design:** Not a public API, but the internal structure is procedural.
* **Error Handling:** Uses `try...except` blocks for handling exceptions, particularly in the AI service module. Errors are logged and user-friendly messages are returned.

## 5. Key Files & Entrypoints

* **Main Entrypoint(s):** `app.py`
* **Configuration:** `config.py` (loads from a user-created `.env` file).
* **CI/CD Pipeline:** None detected.

## 6. Development & Testing Workflow

* **Local Development Environment:**
    1. Create a Python virtual environment.
    2. Install dependencies from `requirements.txt` using `pip`.
    3. Create a `.env` file with `GOOGLE_PROJECT_ID` and `GOOGLE_LOCATION`.
    4. Run the application using `python app.py`.
* **Testing:** No testing framework or test files were detected in the project. This is a critical area for improvement.
* **CI/CD Process:** No CI/CD process is defined.

## 7. Specific Instructions for AI Collaboration

* **Contribution Guidelines:** No `CONTRIBUTING.md` file was found.
* **Infrastructure (IaC):** No Infrastructure as Code (IaC) was detected.
* **Security:** Be mindful of security. Do not hardcode secrets or keys. The project uses `.env` files for this purpose, which are correctly listed in `.gitignore`.
* **Dependencies:** When adding a new dependency, add it to the `requirements.txt` file.
* **Commit Messages:** Follow the Conventional Commits specification (e.g., `feat:`, `fix:`, `docs:`, `refactor:`).
* **Testing:** Any new feature or bug fix should ideally be accompanied by a corresponding test. Since no testing framework is in place, one should be added (e.g., `pytest`).
