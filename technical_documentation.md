# Technical Documentation: AI-Assisted Resume Portfolio Generator

## 1. Project Overview
This project automates the creation of a personal portfolio website from a simple text-based resume. It demonstrates the integration of Python programming, Generative AI (Google Gemini), structured data processing (JSON), and web development (HTML/CSS).

## 2. System Architecture & Data Flow
The core pipeline follows this sequence:

`resume.txt` → **Python** → **Gemini API** → **JSON** → **Python Validation** → `template.html` + `style.css` → `portfolio.html`

### Step-by-Step Flow:
1. **User Input:** The user provides their resume in a plain text file (`resume.txt`).
2. **Python Pre-processing:** `main.py` reads the file, cleans the text (removing extra spaces/empty lines), and checks for valid input.
3. **AI Processing:** The cleaned text is sent to the Google Gemini API with a strict prompt demanding a structured JSON response (no markdown, no hallucinated facts).
4. **Data Extraction:** The Gemini API returns a JSON object containing categorized data (Name, Skills, Experience, etc.).
5. **Validation:** Python parses the JSON to ensure it meets our expected schema and handles any missing fields gracefully.
6. **Web Generation:** Python reads `template.html`, replaces placeholders with the JSON data, and saves the final result as `portfolio.html`.

## 3. Technology Stack Justification

### Python
**Why:** Python is excellent for file manipulation, API interaction, and string processing. It serves as the orchestrator for the entire workflow.

### Google Gemini API
**Why:** Traditional string parsing (like regex) is too rigid for resumes, which come in countless formats. An LLM like Gemini can semantically understand the text and reliably extract structured entities regardless of the original formatting.

### JSON (JavaScript Object Notation)
**Why:** JSON is the standard for data exchange. By forcing Gemini to output JSON, we create a strict contract between the AI's output and our Python code, preventing unpredictable text generation from breaking the HTML builder.

### HTML & CSS (Vanilla)
**Why:** Keeping the web technologies simple (no frameworks like React or Tailwind) ensures the project is easy to understand, modify, and host anywhere. It clearly demonstrates fundamental web concepts.

## 4. File Structure Explanation

* `main.py`: The brain of the operation. Contains the logic to read files, call the API, and write the HTML.
* `resume.txt`: The raw input data.
* `template.html`: The skeleton of the website. Uses placeholders (like `{{name}}`) that Python will find and replace.
* `style.css`: The visual design system for the portfolio.
* `requirements.txt`: Lists external Python libraries needed (e.g., the Gemini SDK).
* `.env` & `.env.example`: Stores secret API keys locally without exposing them in the code.
* `.gitignore`: Tells GitHub which files to ignore (like `.env` and `__pycache__`).
* `AI_USAGE_LOG.md`: A required document detailing how AI assisted in the project's creation.

## 5. Security & Error Handling
* **API Key Security:** The API key is stored in a `.env` file, which is explicitly ignored by `.gitignore` to prevent leaking it on GitHub.
* **Input Validation:** The system must handle empty or excessively short `resume.txt` files before calling the API.
* **AI Hallucination Prevention:** The prompt sent to Gemini explicitly forbids inventing information, ensuring the portfolio strictly reflects the user's actual resume.
