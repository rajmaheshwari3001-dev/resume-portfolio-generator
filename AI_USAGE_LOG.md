# 🤖 AI Usage Log

This document tracks how Artificial Intelligence was utilized in the development of the **AI-Assisted Resume Portfolio Generator**.

| Action | Details |
| :--- | :--- |
| **🛠 Tool Used** | Google Gemini (via Antigravity / Agentic Coding Assistant) |
| **🗣 Prompts Given** | 1. "Build a professional Web App frontend with GSAP and glassmorphism."<br>2. "Implement a FastAPI backend to synthesize the text into JSON securely."<br>3. "Provide a robust JSON parsing logic to protect against Gemini formatting errors." |
| **✨ What Was Generated** | - The core `FastAPI` endpoint connecting to Gemini (`main.py`).<br>- The modern `index.html`, `style.css`, and `script.js`.<br>- The self-contained Bento Box layout inside `template.html`. |
| **🔧 What Was Corrected** | - Adjusted `script.js` to ensure GSAP animations trigger perfectly with the new DOM elements.<br>- Refined the Gemini model string to match `google.generativeai` SDK limits (`gemini-flash-latest`).<br>- Patched `main.py` with `PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION` to fix Python 3.14 alpha crashes. |

---
*Log finalized as per the student brief requirements.*
