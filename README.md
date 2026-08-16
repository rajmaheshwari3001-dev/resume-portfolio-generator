# AI-Assisted Resume Portfolio Generator

A Python-based tool that takes a simple `resume.txt` file, uses the Gemini API to intelligently extract and structure the information, and generates a beautiful, responsive HTML portfolio.

## Setup & Run Instructions
1. Clone this repository.
2. Install the required dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and add your Gemini API key (do not share this key).
4. Place your resume text in `resume.txt`.
5. Run the script: `python main.py`
6. Open `portfolio.html` in your browser.

## Workflow
1. The script reads your resume text from `resume.txt`.
2. It cleans the text and sends it to the Gemini API using a strict prompt.
3. Gemini returns structured JSON data containing your resume sections.
4. Python parses this JSON and injects the values into a predefined HTML template.
5. The final output is saved as `portfolio.html`.

## Prompt Design
The prompt is specifically designed to enforce a strict JSON format. It clearly instructs Gemini not to invent any information (skills, projects, companies, dates) and to use empty values if the information is missing from the provided resume text.

## Limitations & Hallucination Risks
* **Hallucinations:** AI models like Gemini can sometimes "hallucinate" or invent details that are not present in the source text. Although the prompt strictly forbids this, you must ALWAYS verify the generated `portfolio.html` against your original resume.
* **Format Errors:** If Gemini returns invalid JSON, the script will catch the error and stop safely. 
* **Static Template:** The current HTML layout is static and assumes you want to display all provided fields. Missing fields are gracefully hidden.

## Testing Results
* **Missing `resume.txt`:** The script shows a clear error message and stops safely.
* **Empty Resume:** The script rejects the input with a useful message if it is too short.
* **Valid Resume:** The script successfully generates a `portfolio.html` file.
* **Missing Sections:** The script successfully generates only available sections and uses empty strings without crashing.
* **Missing API Key:** Configuration error is shown if the API key is not configured.
* **API / JSON Failure:** Exception handling prevents the program from crashing and logs the issue gracefully.
