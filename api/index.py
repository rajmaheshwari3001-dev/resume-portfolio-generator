import os
import sys
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

# Fix module import for Vercel
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the generation logic from our CLI script
from main import generate_portfolio_html

app = FastAPI()

class ResumeRequest(BaseModel):
    prompt: str
    template: str = "standard"
    theme_color: str = "#6366F1"

@app.post("/api/generate")
async def api_generate(req: ResumeRequest):
    try:
        html = generate_portfolio_html(req.prompt, req.template, req.theme_color)
        return {"html": html}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/")
async def serve_index():
    # Serve the index.html from the parent directory
    parent_dir = os.path.dirname(os.path.dirname(__file__))
    index_path = os.path.join(parent_dir, "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

# For local testing, serve static files (style.css, script.js)
from fastapi.staticfiles import StaticFiles
parent_dir = os.path.dirname(os.path.dirname(__file__))
app.mount("/", StaticFiles(directory=parent_dir, html=False), name="static")
