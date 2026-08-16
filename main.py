"""
main.py
AI-Assisted Resume Portfolio Generator

This is a beginner-friendly script. It reads a resume.txt file, 
asks the Google Gemini AI to extract information from it, 
and then creates a beautiful HTML portfolio website.
"""

import os
import json

# Fix for protobuf compatibility in some Python versions
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

try:
    import google.generativeai as genai
    from dotenv import load_dotenv
except ImportError:
    print("ERROR: Required libraries are missing!")
    print("Please run this command in your terminal first:")
    print("pip install -r requirements.txt\n")
    exit()

def main():
    print("Starting AI-Assisted Resume Portfolio Generator...\n")
    
    # ==========================================
    # STEP 1: Load Environment & API Key
    # ==========================================
    print("Step 1: Checking for API Key...")
    
    # This loads the variables from the .env file
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    
    # Check if the user forgot to add their API key
    if api_key == None or api_key == "your_google_gemini_api_key_here":
        print("\nERROR: API KEY IS MISSING!")
        print("Please open the .env file and paste your real Google Gemini API key.")
        return  # Stop the program here
        
    # Give the API key to the Gemini library
    genai.configure(api_key=api_key)
    print("API Key found! Moving to next step.\n")


    # ==========================================
    # STEP 2: Read and Clean the Resume
    # ==========================================
    print("Step 2: Reading resume.txt...")
    
    # Check if the resume file actually exists
    if not os.path.exists("resume.txt"):
        print("ERROR: Could not find resume.txt!")
        print("Please make sure the file is in the same folder as this script.")
        return # Stop the program
        
    # Open and read the file
    with open("resume.txt", "r") as file:
        resume_text = file.read()
    
    # Clean up the text by removing extra spaces and blank lines
    cleaned_lines = []
    
    # Go through the resume text line by line
    for line in resume_text.split("\n"):
        stripped_line = line.strip() # Remove spaces from the ends of the line
        
        # If the line is not completely empty, keep it
        if stripped_line != "":
            cleaned_lines.append(stripped_line)
            
    # Glue the clean lines back together into one big string
    resume_text = "\n".join(cleaned_lines)
    
    # Check if the resume is too short or empty
    if len(resume_text) < 50:
        print("ERROR: Your resume.txt seems too short or empty.")
        print("Please add more text to it.")
        return # Stop the program
        
    print("Resume read successfully!\n")


    # ==========================================
    # STEP 3: Ask Gemini to Extract Data
    # ==========================================
    print("Step 3: Sending resume to Gemini AI...")
    
    # This prompt tells Gemini EXACTLY what we want
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
    
    # Choose the AI model
    model = genai.GenerativeModel('gemini-flash-latest')
    
    try:
        # Ask the AI
        response = model.generate_content(prompt)
        ai_response_text = response.text
        
        # Sometimes AI adds markdown like ```json, so we remove it
        ai_response_text = ai_response_text.replace('```json', '')
        ai_response_text = ai_response_text.replace('```', '')
        ai_response_text = ai_response_text.strip()
        
        print("AI finished extracting data!\n")
        
    except Exception as error:
        print(f"ERROR: Something went wrong communicating with Gemini: {error}")
        return # Stop the program


    # ==========================================
    # STEP 4: Convert AI Text into Python Data (JSON Validation)
    # ==========================================
    print("Step 4: Validating JSON data...")
    
    try:
        # Convert the text string into a Python Dictionary
        resume_data = json.loads(ai_response_text)
        if type(resume_data) is not dict:
            print("ERROR: The AI returned a list instead of a JSON dictionary.")
            return
        print("Data is valid JSON!\n")
    except Exception as error:
        print("ERROR: The AI did not return valid JSON data.")
        print(f"Details: {error}")
        return # Stop the program


    # ==========================================
    # STEP 5: Generate the Final HTML Website
    # ==========================================
    print("Step 5: Generating portfolio.html...")
    
    if not os.path.exists("template.html"):
        print("ERROR: Could not find template.html!")
        return
        
    # Read the template HTML
    with open("template.html", "r") as template_file:
        html_code = template_file.read()
    
    # Replace simple placeholders using .get() to prevent errors if data is missing
    html_code = html_code.replace("{{name}}", resume_data.get("name", "Your Name"))
    html_code = html_code.replace("{{title}}", resume_data.get("title", "Professional Title"))
    html_code = html_code.replace("{{email}}", resume_data.get("email", "Email not provided"))
    
    # Build About Section
    summary = resume_data.get("summary", "")
    if summary:
        about_html = f"""
        <section id="about">
            <h2>About Me</h2>
            <p>{summary}</p>
        </section>"""
    else:
        about_html = ""
    html_code = html_code.replace("{{about_section}}", about_html)
    
    # Build HTML for Education
    education_list = resume_data.get("education", [])
    if type(education_list) is not list:
        education_list = [education_list] if education_list else []
    if education_list:
        edu_items_html = ""
        for edu in education_list:
            if type(edu) is str:
                edu = {"degree": edu}
            if type(edu) is not dict:
                continue
                
            edu_deg = edu.get("degree", "Degree")
            edu_inst = edu.get("institution", "Institution")
            edu_year = edu.get("year", "")
            
            edu_items_html += f"""
            <div class="education">
                <h3>{edu_deg}</h3>
                <p><strong>{edu_inst}</strong> {edu_year}</p>
            </div>
            """
        education_html = f"""
        <section id="education">
            <h2>Education</h2>
            <div class="education-list">
                {edu_items_html}
            </div>
        </section>"""
    else:
        education_html = ""
    
    html_code = html_code.replace("{{education_section}}", education_html)

    # Build HTML for Experience
    experience_list = resume_data.get("experience", [])
    if type(experience_list) is not list:
        experience_list = [experience_list] if experience_list else []
    if experience_list:
        experience_items_html = ""
        for job in experience_list:
            if type(job) is str:
                job = {"role": job}
            if type(job) is not dict:
                continue
                
            job_role = job.get("role", "Role")
            job_company = job.get("company", "Company")
            job_duration = job.get("duration", "Duration")
            job_desc = job.get("description", "")
            
            experience_items_html += f"""
            <div class="job">
                <h3>{job_role} at {job_company}</h3>
                <p class="duration">{job_duration}</p>
                <p>{job_desc}</p>
            </div>
            """
        experience_html = f"""
        <section id="experience">
            <h2>Experience</h2>
            <div class="experience-list">
                {experience_items_html}
            </div>
        </section>"""
    else:
        experience_html = ""
    
    # Replace the experience placeholder
    html_code = html_code.replace("{{experience_section}}", experience_html)
    
    # Build HTML for Projects
    projects_list = resume_data.get("projects", [])
    if type(projects_list) is not list:
        projects_list = [projects_list] if projects_list else []
    if projects_list:
        projects_items_html = ""
        for proj in projects_list:
            if type(proj) is str:
                proj = {"title": proj}
            if type(proj) is not dict:
                continue
                
            proj_title = proj.get("title", "Project")
            proj_desc = proj.get("description", "")
            proj_tech = proj.get("technologies", "")
            
            projects_items_html += f"""
            <div class="project">
                <h3>{proj_title}</h3>
                <p>{proj_desc}</p>
                <p><strong>Technologies:</strong> {proj_tech}</p>
            </div>
            """
        projects_html = f"""
        <section id="projects">
            <h2>Projects</h2>
            <div class="projects-list">
                {projects_items_html}
            </div>
        </section>"""
    else:
        projects_html = ""
    
    html_code = html_code.replace("{{projects_section}}", projects_html)

    # Build HTML for Skills
    skills_list = resume_data.get("skills", [])
    if type(skills_list) is not list:
        skills_list = [skills_list] if skills_list else []
    if skills_list:
        skills_items_html = ""
        for skill in skills_list:
            skills_items_html += f"<li>{skill}</li>"
            
        skills_html = f"""
        <section id="skills">
            <h2>Skills</h2>
            <ul class="skills-list">
                {skills_items_html}
            </ul>
        </section>"""
    else:
        skills_html = ""
        
    # Replace the skills placeholder
    html_code = html_code.replace("{{skills_section}}", skills_html)

    # Build HTML for Achievements
    achievements_list = resume_data.get("achievements", [])
    if type(achievements_list) is not list:
        achievements_list = [achievements_list] if achievements_list else []
    if achievements_list:
        achievements_items_html = ""
        for ach in achievements_list:
            achievements_items_html += f"<li>{ach}</li>"
            
        achievements_html = f"""
        <section id="achievements">
            <h2>Achievements</h2>
            <ul class="achievements-list">
                {achievements_items_html}
            </ul>
        </section>"""
    else:
        achievements_html = ""
        
    html_code = html_code.replace("{{achievements_section}}", achievements_html)

    # Build Contact details
    phone = resume_data.get("phone", "")
    if phone:
        phone_html = f"<p>Phone: {phone}</p>"
    else:
        phone_html = ""
    html_code = html_code.replace("{{phone_section}}", phone_html)
    
    linkedin = resume_data.get("linkedin", "")
    github = resume_data.get("github", "")
    links_html = ""
    if linkedin or github:
        links_html += "<p>Links: "
        if linkedin:
            links_html += f"<a href='{linkedin}'>LinkedIn</a> "
        if github:
            links_html += f"<a href='{github}'>GitHub</a>"
        links_html += "</p>"
    
    html_code = html_code.replace("{{links_section}}", links_html)
    
    # Save the final website file
    with open("portfolio.html", "w") as output_file:
        output_file.write(html_code)
    
    print("SUCCESS! Your portfolio has been generated.")
    print("Open 'portfolio.html' in your browser to see the result!")

# This line just tells Python to run the main() function when we start the script
if __name__ == "__main__":
    main()
