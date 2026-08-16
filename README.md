<div align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" />
  <img src="https://img.shields.io/badge/Gemini_AI-4285F4?style=for-the-badge&logo=google&logoColor=white" />
  <img src="https://img.shields.io/badge/GSAP-88CE02?style=for-the-badge&logo=greensock&logoColor=white" />
  
  <br />
  
  <h1>✨ AI Portfolio Architect</h1>
  <p><b>Transform raw text into an award-winning, stunning portfolio in seconds.</b></p>
</div>

---

## 🌟 The Vision
The **AI Portfolio Architect** goes far beyond standard resume parsers. Built with a luxurious, custom-cursor, magnetic-hover frontend and powered by a robust Python/FastAPI backend, it uses the **Google Gemini API** to synthesize unstructured text into a fully formatted, portable HTML masterpiece.

## 🚀 Key Features
- **Insane UI/UX**: Custom haptics, GSAP animations, magnetic buttons, and glassmorphism panels.
- **AI-Powered Synthesis**: Gemini accurately extracts Education, Experience, Skills, and Projects without hallucination.
- **Portable Export**: Instantly download a 100% self-contained `portfolio.html` with beautiful embedded styling.
- **Zero-Config Deployment**: Built specifically to deploy perfectly on Vercel as a serverless Python function.

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
