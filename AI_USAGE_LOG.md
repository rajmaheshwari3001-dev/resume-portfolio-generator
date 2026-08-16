# 🤖 AI Usage Log

This document tracks how Artificial Intelligence was utilized as a pair-programming assistant during the development of the **AI-Assisted Resume Portfolio Generator**.

| Action | Details |
| :--- | :--- |
| **🛠 Tool Used** | Google Gemini (via Agentic Coding Assistant) |
| **🗣 Prompts Given** | 1. "Assist in defining a strict JSON schema for the Google GenAI extraction prompt to prevent data hallucination."<br>2. "Provide logic for an exponential backoff loop to gracefully handle API 503 high-demand errors."<br>3. "Help structure a responsive HTML grid layout for the `template.html` file." |
| **✨ What Was Generated** | - Baseline boilerplate for the `google-genai` SDK integration.<br>- The skeleton layout of the HTML/CSS template.<br>- The `try/except` loop logic in Python to manage server retries. |
| **🔧 What Was Corrected** | - Refactored the generated Python script to strictly run locally via the CLI as per the project rubric requirements.<br>- Stripped out unnecessary web server frameworks (FastAPI) to ensure the codebase remains purely focused on local JSON extraction and HTML generation.<br>- Manually customized the CSS to achieve the final premium aesthetic. |

---
*Log finalized in compliance with project brief guidelines.*
