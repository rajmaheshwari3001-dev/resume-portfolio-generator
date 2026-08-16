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

## 🌟 The Project
The **AI-Assisted Resume Portfolio Generator** uses the **Google Gemini API** to synthesize unstructured resume text into a fully formatted, portable HTML portfolio. Built with a clean Python/FastAPI backend and a modern web interface.

## 🚀 Key Features
- **Clean UI/UX**: Straightforward, professional interface for rapid portfolio generation.
- **AI-Powered Extraction**: Gemini accurately extracts Education, Experience, Skills, and Projects from plain text.
- **Portable Export**: Instantly download a 100% self-contained `portfolio.html` with a beautiful Bento Box layout and embedded CSS.
- **Zero-Config Deployment**: Built to deploy seamlessly on serverless platforms like Vercel.

## 🛠 Setup & Run Instructions

### Local Environment
1. Clone this repository.
2. Install dependencies: 
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and paste your Gemini API key:
   ```env
   GEMINI_API_KEY=your_key_here
   ```
4. Start the synthesis engine:
   ```bash
   uvicorn main:app --reload
   ```
5. Open `http://localhost:8000` in your browser.

## 🧠 Prompt Architecture
Our prompt rigorously enforces a strict JSON format. It aggressively commands Gemini to **never invent data** (hallucinate). Missing fields are intelligently handled and safely suppressed in the final HTML.

## ⚠️ Limitations
* **Hallucination Risk:** Although strongly suppressed, generative AI can sometimes hallucinate. Always review the downloaded portfolio.
* **Layout:** The current template layout is fixed, dynamically hiding sections that lack data.

---
<div align="center">
<i>Built with precision for the modern developer.</i>
</div>
