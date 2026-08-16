import os
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"
import json
import google.generativeai as genai
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI()

# Mount static files (css, js, images) from the current directory
# Since we will serve index.html directly from a route, we mount the rest under /static if needed, 
# or just serve them manually to avoid conflicts with Vercel's static handling.

class ResumeRequest(BaseModel):
    prompt: str

def generate_portfolio_html(resume_text: str) -> str:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise Exception("API key is not configured on the server.")
        
    genai.configure(api_key=api_key)
    
    prompt = f"""
    You are a strict data extraction assistant.
    Extract information from the provided resume text.
    You MUST respond with valid JSON ONLY. 
    Do NOT invent skills, experience, projects, achievements, companies, dates, or links. 
    If something is missing, leave it empty.

    Required JSON Format:
    {{
      "name": "Full Name",
      "title": "Professional Title",
      "email": "Email Address",
      "phone": "Phone Number",
      "linkedin": "LinkedIn URL",
      "github": "GitHub URL",
      "summary": "A short summary",
      "education": [
        {{
          "degree": "Degree Name",
          "institution": "Institution Name",
          "year": "Year"
        }}
      ],
      "experience": [
        {{
          "role": "Job Title",
          "company": "Company Name",
          "duration": "Duration",
          "description": "Job Description"
        }}
      ],
      "projects": [
        {{
          "title": "Project Title",
          "description": "Project Description",
          "technologies": "Technologies used"
        }}
      ],
      "achievements": ["Achievement 1", "Achievement 2"],
      "skills": ["Skill 1", "Skill 2"]
    }}

    Resume Text:
    {resume_text}
    """
    
    model = genai.GenerativeModel('gemini-flash-latest')
    response = model.generate_content(prompt, generation_config={"temperature": 0.4})
    ai_response_text = response.text.replace('```json', '').replace('```', '').strip()
    
    resume_data = json.loads(ai_response_text)
    
    template_path = os.path.join(os.path.dirname(__file__), "template.html")
    if not os.path.exists(template_path):
        raise Exception("Template file not found.")
        
    with open(template_path, "r") as f:
        html_code = f.read()
        
    html_code = html_code.replace("{{name}}", resume_data.get("name", "Your Name"))
    html_code = html_code.replace("{{title}}", resume_data.get("title", "Professional Title"))
    html_code = html_code.replace("{{email}}", resume_data.get("email", "Email not provided"))
    
    summary = resume_data.get("summary", "")
    about_html = f'<p>{summary}</p>' if summary else ""
    html_code = html_code.replace("{{about_section}}", about_html)
    
    edu_list = resume_data.get("education", [])
    edu_html = ''
    if isinstance(edu_list, list):
        for edu in edu_list:
            if isinstance(edu, dict):
                edu_html += f'<div class="education"><h3>{edu.get("degree", "")}</h3><p><strong>{edu.get("institution", "")}</strong> {edu.get("year", "")}</p></div>'
    html_code = html_code.replace("{{education_section}}", edu_html)

    # Experience
    exp_list = resume_data.get("experience", [])
    exp_html = ''
    if isinstance(exp_list, list):
        for exp in exp_list:
            if isinstance(exp, dict):
                exp_html += f'<div class="job"><h3>{exp.get("role", "")} at {exp.get("company", "")}</h3><p class="duration">{exp.get("duration", "")}</p><p>{exp.get("description", "")}</p></div>'
    html_code = html_code.replace("{{experience_section}}", exp_html)

    # Projects
    proj_list = resume_data.get("projects", [])
    proj_html = ''
    if isinstance(proj_list, list):
        for proj in proj_list:
            if isinstance(proj, dict):
                proj_html += f'<div class="project"><h3>{proj.get("title", "")}</h3><p>{proj.get("description", "")}</p><p style="margin-top:0.5rem"><strong>Technologies:</strong> {proj.get("technologies", "")}</p></div>'
    html_code = html_code.replace("{{projects_section}}", proj_html)

    # Skills
    skills_list = resume_data.get("skills", [])
    skills_html = '<ul>' if skills_list else ''
    if isinstance(skills_list, list):
        for skill in skills_list:
            skills_html += f'<li>{skill}</li>'
    if skills_list: skills_html += '</ul>'
    html_code = html_code.replace("{{skills_section}}", skills_html)

    # Achievements
    achievements_list = resume_data.get("achievements", [])
    achievements_html = '<ul>' if achievements_list else ''
    if isinstance(achievements_list, list):
        for ach in achievements_list:
            achievements_html += f'<li style="list-style:disc; margin-left:20px; margin-bottom:5px">{ach}</li>'
    if achievements_list: achievements_html += '</ul>'
    html_code = html_code.replace("{{achievements_section}}", achievements_html)

    phone = resume_data.get("phone", "")
    html_code = html_code.replace("{{phone_section}}", f'<div class="contact-item"><span>Phone</span><a href="tel:{phone}">{phone}</a></div>' if phone else "")
    
    linkedin = resume_data.get("linkedin", "")
    github = resume_data.get("github", "")
    links_html = "<p>Links: "
    if linkedin: links_html += f"<a href='{linkedin}'>LinkedIn</a> "
    if github: links_html += f"<a href='{github}'>GitHub</a>"
    links_html += "</p>" if (linkedin or github) else ""
    html_code = html_code.replace("{{links_section}}", links_html)

    return html_code

@app.post("/api/generate")
async def api_generate(req: ResumeRequest):
    try:
        html = generate_portfolio_html(req.prompt)
        return {"html": html}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/")
async def serve_index():
    with open(os.path.join(os.path.dirname(__file__), "index.html"), "r") as f:
        return HTMLResponse(content=f.read())

if __name__ == "__main__":
    import sys
    print("--- Local CLI Mode ---")
    resume_path = "resume.txt"
    if not os.path.exists(resume_path):
        print(f"Error: {resume_path} not found. Please create it first.")
        sys.exit(1)
        
    print(f"Reading {resume_path}...")
    with open(resume_path, "r", encoding="utf-8") as f:
        resume_text = f.read()
        
    print("Synthesizing portfolio with Gemini AI...")
    try:
        final_html = generate_portfolio_html(resume_text)
        with open("portfolio.html", "w", encoding="utf-8") as f:
            f.write(final_html)
        print("Success! Generated portfolio.html")
    except Exception as e:
        print(f"Failed to generate portfolio: {e}")
