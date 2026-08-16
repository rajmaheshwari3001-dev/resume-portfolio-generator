<div align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" />
  <img src="https://img.shields.io/badge/Gemini_AI-4285F4?style=for-the-badge&logo=google&logoColor=white" />
  <img src="https://img.shields.io/badge/GSAP-88CE02?style=for-the-badge&logo=greensock&logoColor=white" />
  
  <br />
  
  <h1>AI-Assisted Resume Portfolio Generator</h1>
  <p><b>Transform your resume into a clean, professional, and portable portfolio webpage in seconds.</b></p>
</div>

---

# AI-Assisted Resume Portfolio Generator

A fully autonomous Python command-line tool that parses an unstructured `resume.txt` file and leverages Google's Gemini AI to synthesize a beautifully structured HTML portfolio.

## ✨ Features
*   **Intelligent Data Extraction:** Uses Gemini AI to accurately extract semantic meaning (experience, education, skills, projects) from plain text.
*   **Strict JSON Enforcement:** The model is aggressively prompted to return ONLY valid JSON and to never hallucinate data.
*   **Automated HTML Generation:** Injects the synthesized JSON data into a clean, modern `template.html`.
*   **High-Demand Resilience:** Includes an automatic exponential backoff/retry loop to gracefully handle Google API `503 UNAVAILABLE` errors.

## 🛠 Setup & Run Instructions

### Prerequisites
1. Python 3.10+
2. A Gemini API Key from Google AI Studio.

### Local Installation
1. Clone this repository to your local machine.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and paste your Gemini API key:
   ```env
   GEMINI_API_KEY=your_key_here
   ```

### Running the Generator
1. Ensure your resume text is saved inside `resume.txt` in the project root.
2. Run the script:
   ```bash
   python main.py
   ```
3. The console will read the text, synthesize the portfolio, and automatically handle any AI server load spikes.
4. When successful, a `portfolio.html` file will be generated in the same directory! Double-click it to view your stunning portfolio in any web browser.

## 🧠 Prompt Architecture & Defense
Our prompt rigorously enforces a strict JSON format. It explicitly commands the Gemini model to **never invent data** (hallucinate). Missing fields are intelligently handled and safely suppressed in the final HTML. The system uses Google's modern `google-genai` SDK and defaults to `gemini-flash-latest` for optimal speed and extraction accuracy.

## 👥 Contributors
- Rajesh Kumar

---
<div align="center">
<i>Built with precision for the modern developer.</i>
</div>
