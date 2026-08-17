# 🤖 AI Usage Log

This document tracks how Artificial Intelligence was utilized as a pair-programming assistant during the development of the **AI-Assisted Resume Portfolio Generator**.

| Action | Details |
| :--- | :--- |
| **🛠 Tool Used** | Google Gemini (via Agentic Coding Assistant) |
| **🗣 Prompts Given** | 1. "Assist in defining a strict JSON schema for the Google GenAI extraction prompt to prevent data hallucination."<br>2. "Provide logic for an exponential backoff loop to gracefully handle API 503 high-demand errors."<br>3. "Help structure a responsive HTML grid layout for the `template.html` file."<br>4. "Create a design thinking plan to improve the UI/UX with modern fonts and a better theme."<br>5. "Why is the chatbot giving the same answer every time? Improve their latency and messaging style."<br>6. "Add a feature to select portfolio themes (Glassmorphism, Cyberpunk, Neobrutalism)."<br>7. "Improve the theme of the landing page to have brighter vibes." |
| **✨ What Was Generated** | - Baseline boilerplate for the SDK integration.<br>- The skeleton layout of the HTML/CSS template, and later the "Brighter Vibes" redesign with frosty glassmorphism panels, premium fonts (`Plus Jakarta Sans`), and glowing sunset blobs.<br>- The `try/except` loop logic in Python to manage server retries.<br>- Improved conversational AI prompt and history mapping for the portfolio chatbot.<br>- A fully functional Theme Card selection UI that dynamically injects CSS template classes into the generated portfolio. |
| **🔧 What Was Corrected** | - Refactored the generated Python script to strictly run locally via the CLI as per the project rubric requirements.<br>- Stripped out unnecessary web server frameworks to ensure the codebase remains purely focused on local JSON extraction and HTML generation.<br>- **Critical Bug Fix:** Removed the `google-generativeai` pip dependencies entirely, migrating to raw Python `requests` to the Gemini REST API.<br>- **Validation Fix:** Removed the strict 40-word limit minimum to allow shorter resumes, and added a robust fallback logic to handle resumes that omit the candidate's name. |

---
*Log finalized in compliance with project brief guidelines.*
