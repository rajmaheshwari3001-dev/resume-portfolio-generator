# AI Usage Log

## AI Tool Used
Google Gemini (via Antigravity / Agentic Coding Assistant)

## Prompt or Request Given to the Tool
- "Create a Python script to parse a resume and generate a portfolio HTML using the Gemini API."
- "Refine the JSON output format so it precisely matches the required structure."
- "Create a clean, modern CSS style for the generated portfolio template."

## What the Tool Generated
- The core structure of `main.py` including the file reading, API connection, and HTML generation.
- The prompt engineering logic to force Gemini to return strict JSON.
- The initial layout and CSS for `template.html` and `style.css`.

## What Was Changed or Corrected
- Fixed compatibility issues with `google.generativeai` and `protobuf` by adding the `PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION` environment variable override.
- Separated the embedded CSS in `template.html` into a standalone `style.css` file to strictly meet project requirements.
- Corrected the Gemini model string to match the supported version for the installed SDK (`gemini-flash-latest`).
