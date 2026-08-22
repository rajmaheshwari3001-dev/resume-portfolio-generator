import os
import json
import requests
import warnings
import logging
warnings.filterwarnings("ignore")
logging.getLogger().setLevel(logging.ERROR)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

html_code_cache = None

def generate_portfolio_html(resume_text: str, template: str = "standard", theme_color: str = "#6366F1") -> tuple:
    # Remove unnecessary spaces and blank lines (Rubric requirement)
    cleaned_resume_text = "\n".join([line.strip() for line in resume_text.split('\n') if line.strip()])
    
    if not cleaned_resume_text:
        raise Exception("Resume text cannot be empty.")

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise Exception("API key is not configured on the server.")
    
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
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-lite-latest:generateContent?key={api_key}"
    
    payload = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.4,
            "responseMimeType": "application/json"
        }
    }
    
    import time
    max_retries = 3
    ai_response_text = ""
    success = False
    last_gemini_error = ""

    for attempt in range(max_retries):
        response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
        if response.status_code == 200:
            data = response.json()
            ai_response_text = data["candidates"][0]["content"]["parts"][0]["text"].replace('```json', '').replace('```', '').strip()
            success = True
            break
        elif response.status_code == 503 and attempt < max_retries - 1:
            time.sleep(2)  # Short 2-second sleep for serverless environments
            continue
        else:
            last_gemini_error = f"Gemini API Error: {response.status_code} - {response.text}"
            break
            
    if not success:
        grok_api_key = os.environ.get("GROK_API_KEY")
        if grok_api_key:
            grok_url = "https://api.x.ai/v1/chat/completions"
            grok_payload = {
                "model": "grok-beta",
                "messages": [
                    {"role": "system", "content": "You are a strict data extraction assistant. You MUST respond with valid JSON ONLY."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.4
            }
            grok_headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {grok_api_key}"
            }
            grok_response = requests.post(grok_url, json=grok_payload, headers=grok_headers)
            if grok_response.status_code == 200:
                data = grok_response.json()
                ai_response_text = data["choices"][0]["message"]["content"].replace('```json', '').replace('```', '').strip()
            else:
                raise Exception(f"{last_gemini_error} | Grok Fallback Failed: {grok_response.status_code} - {grok_response.text}")
        else:
            raise Exception(last_gemini_error)
    
    resume_data = json.loads(ai_response_text)
    
    global html_code_cache
    if html_code_cache is None:
        template_path = os.path.join(os.path.dirname(__file__), "template.html")
        if not os.path.exists(template_path):
            template_path = "template.html"
            if not os.path.exists(template_path):
                raise Exception("template.html file not found.")
        with open(template_path, "r", encoding="utf-8") as f:
            html_code_cache = f.read()
    
    html_code = html_code_cache

    # Inject Theme and Template Class
    # Calculate RGB for rgba() usage in CSS
    hex_color = theme_color.lstrip('#')
    try:
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        rgb_str = f"{r}, {g}, {b}"
    except:
        rgb_str = "6, 182, 212" # Fallback cyan

    theme_style = f"<style>:root {{ --accent-color: {theme_color} !important; --accent: {theme_color} !important; --accent-color-rgb: {rgb_str} !important; }}</style>"
    html_code = html_code.replace("</head>", f"    {theme_style}\n</head>")
    html_code = html_code.replace("<body>", f"<body class='template-{template}'>")
        
    warnings = []
    
    name = resume_data.get("name")
    if not name or name.strip() == "" or "your name" in name.lower() or "applicant" in name.lower():
        warnings.append("Name")
        name = "Name Not Provided"
    
    email = resume_data.get("email")
    phone = resume_data.get("phone")
    linkedin = resume_data.get("linkedin")
    github = resume_data.get("github")
    
    if not email and not phone:
        warnings.append("Contact (Email or Phone)")
        
    if not linkedin:
        warnings.append("LinkedIn")
        
    # Dynamically inject the extracted JSON data into the HTML template placeholders
    html_code = html_code.replace("{{name}}", name)
    
    title = resume_data.get("title")
    if not title or title.strip() == "":
        title = "Professional Title"
    html_code = html_code.replace("{{title}}", title)
    
    email = resume_data.get("email")
    if not email or email.strip() == "":
        email = "Email not provided"
    html_code = html_code.replace("{{email}}", email)
    
    summary = resume_data.get("summary", "")
    about_html = f'<p>{summary}</p>' if summary else ""
    html_code = html_code.replace("{{about_section}}", about_html)
    
    edu_list = resume_data.get("education", [])
    achievements_list = resume_data.get("achievements", [])
    edu_achievements_html = ''
    has_edu = isinstance(edu_list, list) and len(edu_list) > 0
    has_ach = isinstance(achievements_list, list) and len(achievements_list) > 0
    if has_edu or has_ach:
        edu_achievements_html = '<section id="education" class="section-container" aria-label="Education and Achievements">'
        if has_edu:
            edu_achievements_html += '<h2 class="section-title">Education</h2>'
            for edu in edu_list:
                if isinstance(edu, dict):
                    edu_achievements_html += f'<div class="timeline-item"><h3>{edu.get("degree", "")}</h3><p class="duration">{edu.get("institution", "")} &bull; {edu.get("year", "")}</p></div>'
        if has_edu and has_ach:
            edu_achievements_html += '<br>'
        if has_ach:
            edu_achievements_html += '<h2 class="section-title">Achievements</h2><ul class="achievements-list">'
            for ach in achievements_list:
                edu_achievements_html += f'<li>{ach}</li>'
            edu_achievements_html += '</ul>'
        edu_achievements_html += '</section>'
    html_code = html_code.replace("{{education_achievements_section}}", edu_achievements_html)

    # Experience
    exp_list = resume_data.get("experience", [])
    exp_html = ''
    if isinstance(exp_list, list) and len(exp_list) > 0:
        exp_html = '<section id="experience" class="section-container" aria-label="Work Experience"><h2 class="section-title">Experience</h2>'
        for exp in exp_list:
            if isinstance(exp, dict):
                exp_html += f'<div class="timeline-item"><h3>{exp.get("role", "")} at {exp.get("company", "")}</h3><p class="duration">{exp.get("duration", "")}</p><p>{exp.get("description", "")}</p></div>'
        exp_html += '</section>'
    html_code = html_code.replace("{{experience_section}}", exp_html)

    # Projects
    proj_list = resume_data.get("projects", [])
    proj_html = ''
    if isinstance(proj_list, list) and len(proj_list) > 0:
        proj_html = '<section id="projects" class="section-container" aria-label="Projects"><h2 class="section-title">Featured Projects</h2><div class="projects-grid">'
        for proj in proj_list:
            if isinstance(proj, dict):
                proj_html += f'<div class="project-card"><h3>{proj.get("title", "")}</h3><p>{proj.get("description", "")}</p><div class="tech-tags">{proj.get("technologies", "")}</div></div>'
        proj_html += '</div></section>'
    html_code = html_code.replace("{{projects_section}}", proj_html)

    # Skills
    skills_list = resume_data.get("skills", [])
    skills_html = ''
    if isinstance(skills_list, list) and len(skills_list) > 0:
        skills_html = '<section id="skills" class="section-container" aria-label="Skills"><h2 class="section-title">Core Competencies</h2><div class="skills-container">'
        for skill in skills_list:
            skills_html += f'<div class="skill-tag">{skill}</div>'
        skills_html += '</div></section>'
    html_code = html_code.replace("{{skills_section}}", skills_html)

    phone = resume_data.get("phone", "")
    html_code = html_code.replace("{{phone_section}}", f'<div class="contact-item"><i data-lucide="phone"></i><a href="tel:{phone}">{phone}</a></div>' if phone else "")
    
    linkedin = resume_data.get("linkedin", "")
    github = resume_data.get("github", "")
    links_html = ""
    if linkedin: 
        links_html += f'<div class="contact-item"><i data-lucide="linkedin"></i><a href="{linkedin}">LinkedIn</a></div>'
    if github: 
        links_html += f'<div class="contact-item"><i data-lucide="github"></i><a href="{github}">GitHub</a></div>'
    
    html_code = html_code.replace("{{links_section}}", links_html)

    hero_links_html = ""
    if linkedin or github:
        hero_links_html = '<div class="hero-socials">'
        if github: 
            hero_links_html += f'<a href="{github}" class="social-icon"><i data-lucide="github"></i></a>'
        if linkedin: 
            hero_links_html += f'<a href="{linkedin}" class="social-icon"><i data-lucide="linkedin"></i></a>'
        hero_links_html += '</div>'
    html_code = html_code.replace("{{hero_links_section}}", hero_links_html)

    return html_code, warnings

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
            final_html, warnings = generate_portfolio_html(resume_text)
            if warnings:
                print("Warnings:", ", ".join(warnings))
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
