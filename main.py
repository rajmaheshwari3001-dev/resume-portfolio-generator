import os
import json
import warnings
import logging
warnings.filterwarnings("ignore")
logging.getLogger().setLevel(logging.ERROR)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from google import genai

def generate_portfolio_html(resume_text: str) -> str:
    # Remove unnecessary spaces and blank lines (Rubric requirement)
    cleaned_resume_text = "\n".join([line.strip() for line in resume_text.split('\n') if line.strip()])
    
    word_count = len(cleaned_resume_text.split())
    if word_count < 40:
        raise Exception(f"Resume text is too short ({word_count} words). Minimum 40 words required for a professional portfolio.")

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise Exception("API key is not configured on the server.")
        
    client = genai.Client(api_key=api_key)
    
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
    {cleaned_resume_text}
    """
    
    response = client.models.generate_content(
        model='gemini-flash-latest',
        contents=prompt,
        config=genai.types.GenerateContentConfig(temperature=0.4)
    )
    ai_response_text = response.text.replace('```json', '').replace('```', '').strip()
    
    resume_data = json.loads(ai_response_text)
    
    # We must find template.html relative to this file, or the CWD
    template_path = os.path.join(os.path.dirname(__file__), "template.html")
    if not os.path.exists(template_path):
        # Fallback to CWD if running from a different context
        template_path = "template.html"
        if not os.path.exists(template_path):
            raise Exception("template.html file not found.")
        
    with open(template_path, "r", encoding="utf-8") as f:
        html_code = f.read()
        
    html_code = html_code.replace("{{name}}", resume_data.get("name", "Your Name"))
    html_code = html_code.replace("{{title}}", resume_data.get("title", "Professional Title"))
    html_code = html_code.replace("{{email}}", resume_data.get("email", "Email not provided"))
    
    summary = resume_data.get("summary", "")
    about_html = f'<p>{summary}</p>' if summary else ""
    html_code = html_code.replace("{{about_section}}", about_html)
    
    edu_list = resume_data.get("education", [])
    achievements_list = resume_data.get("achievements", [])
    edu_achievements_html = ''
    has_edu = isinstance(edu_list, list) and len(edu_list) > 0
    has_ach = isinstance(achievements_list, list) and len(achievements_list) > 0
    if has_edu or has_ach:
        edu_achievements_html = '<section class="bento-card card-education" aria-label="Education and Achievements">'
        if has_edu:
            edu_achievements_html += '<div class="card-header">Education</div>'
            for edu in edu_list:
                if isinstance(edu, dict):
                    edu_achievements_html += f'<div class="education"><h3>{edu.get("degree", "")}</h3><p><strong>{edu.get("institution", "")}</strong> {edu.get("year", "")}</p></div>'
        if has_edu and has_ach:
            edu_achievements_html += '<br>'
        if has_ach:
            edu_achievements_html += '<div class="card-header">Achievements</div><ul>'
            for ach in achievements_list:
                edu_achievements_html += f'<li style="list-style:disc; margin-left:20px; margin-bottom:5px">{ach}</li>'
            edu_achievements_html += '</ul>'
        edu_achievements_html += '</section>'
    html_code = html_code.replace("{{education_achievements_section}}", edu_achievements_html)

    # Experience
    exp_list = resume_data.get("experience", [])
    exp_html = ''
    if isinstance(exp_list, list) and len(exp_list) > 0:
        exp_html = '<section class="bento-card card-experience" aria-label="Work Experience"><div class="card-header">Experience</div>'
        for exp in exp_list:
            if isinstance(exp, dict):
                exp_html += f'<div class="job"><h3>{exp.get("role", "")} at {exp.get("company", "")}</h3><p class="duration">{exp.get("duration", "")}</p><p>{exp.get("description", "")}</p></div>'
        exp_html += '</section>'
    html_code = html_code.replace("{{experience_section}}", exp_html)

    # Projects
    proj_list = resume_data.get("projects", [])
    proj_html = ''
    if isinstance(proj_list, list) and len(proj_list) > 0:
        proj_html = '<section class="card-projects" aria-label="Projects">'
        for proj in proj_list:
            if isinstance(proj, dict):
                proj_html += f'<div class="project"><h3>{proj.get("title", "")}</h3><p>{proj.get("description", "")}</p><p style="margin-top:0.5rem"><strong>Technologies:</strong> {proj.get("technologies", "")}</p></div>'
        proj_html += '</section>'
    html_code = html_code.replace("{{projects_section}}", proj_html)

    # Skills
    skills_list = resume_data.get("skills", [])
    skills_html = ''
    if isinstance(skills_list, list) and len(skills_list) > 0:
        skills_html = '<section class="bento-card card-skills" aria-label="Skills"><div class="card-header">Core Competencies</div><ul>'
        for skill in skills_list:
            skills_html += f'<li>{skill}</li>'
        skills_html += '</ul></section>'
    html_code = html_code.replace("{{skills_section}}", skills_html)

    phone = resume_data.get("phone", "")
    html_code = html_code.replace("{{phone_section}}", f'<div class="contact-item"><span>Phone</span><a href="tel:{phone}">{phone}</a></div>' if phone else "")
    
    linkedin = resume_data.get("linkedin", "")
    github = resume_data.get("github", "")
    links_html = ""
    if linkedin or github:
        links_html = "<p>Links: "
        if linkedin: links_html += f"<a href='{linkedin}'>LinkedIn</a> "
        if github: links_html += f"<a href='{github}'>GitHub</a>"
        links_html += "</p>"
    html_code = html_code.replace("{{links_section}}", links_html)

    return html_code

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
    import time
    max_retries = 5
    for attempt in range(max_retries):
        try:
            final_html = generate_portfolio_html(resume_text)
            with open("portfolio.html", "w", encoding="utf-8") as f:
                f.write(final_html)
            print("Success! Generated portfolio.html")
            break
        except Exception as e:
            error_str = str(e)
            if "503" in error_str and attempt < max_retries - 1:
                print(f"Model is experiencing high demand (503). Retrying in 5 seconds... (Attempt {attempt + 1}/{max_retries})")
                time.sleep(5)
            else:
                print(f"Failed to generate portfolio: {e}")
                break
