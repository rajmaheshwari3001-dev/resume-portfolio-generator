# Code Explanation: Resume Portfolio Generator

This document explains how the `main.py` script works, step by step, in simple terms so you can understand and explain it to anyone (like an instructor or your bootcamp group).

## 1. The Setup (Imports)
```python
import os
import json
try:
    import google.generativeai as genai
    from dotenv import load_dotenv
...
```
* **`os`**: A built-in Python library used to check if files exist (like `resume.txt`) and to read environment variables.
* **`json`**: A built-in Python library used to convert text data into Python dictionaries.
* **`google.generativeai`**: The official library to talk to Google's Gemini AI.
* **`dotenv`**: A library that secretly loads variables (like your API key) from the `.env` file into your program so you don't have to hardcode passwords in your script.

## 2. Step 1: Loading the API Key
```python
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
...
genai.configure(api_key=api_key)
```
Here, we read the `.env` file to find `GEMINI_API_KEY`. If the key is missing or is the default template string, the script stops safely. If it finds the key, it hands it over to the Gemini library (`genai.configure`) to log us in.

## 3. Step 2: Reading the Resume
```python
with open("resume.txt", "r") as file:
    resume_text = file.read()
```
We use standard Python's `with open(...)` to open the `resume.txt` file in "read" mode (`"r"`). Using `with` is a best practice because it automatically closes the file for us when it's done reading, even if an error happens. We then clean out extra spaces and check if the resume is too short (less than 50 characters).

## 4. Step 3: Asking Gemini (Prompt Engineering)
```python
prompt = f"""
You are a strict data extraction assistant...
"""
model = genai.GenerativeModel('gemini-flash-latest')
response = model.generate_content(prompt)
```
This is the core of the AI logic! We define a strict "prompt" telling Gemini exactly what we want. We provide a JSON template for it to fill out and explicitly tell it *not* to invent information. 
We ask for the `gemini-flash-latest` model (which is fast and free) and then ask the AI to generate the content based on our prompt. We clean up the response by removing any markdown (like ` ```json `) that Gemini sometimes adds.

## 5. Step 4: Parsing and Bulletproofing the Data
```python
resume_data = json.loads(ai_response_text)
if type(resume_data) is not dict: ...
```
We use `json.loads()` to convert the text response from Gemini into a real Python Dictionary. 
AI models sometimes "hallucinate" and return the wrong format (like returning a list instead of a dictionary). We added `if type(resume_data) is not dict:` as a safety net to catch those mistakes and stop the program safely rather than crashing.

## 6. Step 5: Generating the HTML Website
```python
template_file = open("template.html", "r", encoding="utf-8")
html_code = template_file.read()
```
We open our `template.html` file, which contains placeholders like `{{name}}` and `{{skills_section}}`.

```python
html_code = html_code.replace("{{name}}", resume_data.get("name", "Your Name"))
```
We use the `.get()` method to safely pull data from the dictionary. If Gemini forgot to include the "name" field, `.get()` safely defaults to `"Your Name"` instead of crashing. We then use `.replace()` to swap the placeholder `{{name}}` with the real name.

### Bulletproofing the Lists (Education, Experience, etc.)
```python
education_list = resume_data.get("education", [])
if type(education_list) is not list:
    education_list = [education_list] if education_list else []
```
Sometimes Gemini messes up and returns a single text string instead of a list. If we try to loop through a string like a list, the program crashes! 
This specific block checks: *"Is this actually a list? If not, forcefully wrap it in a list [ ] so our loop doesn't crash."*

```python
for edu in education_list:
    edu_deg = edu.get("degree", "Degree")
    ...
    edu_items_html += f"""<div class="education">...</div>"""
```
We loop through the safe list, grab the details (like degree and institution), and glue them together into chunks of HTML code using Python f-strings (`f"..."`).

```python
output_file = open("portfolio.html", "w", encoding="utf-8")
output_file.write(html_code)
output_file.close()
```
Finally, once all placeholders are replaced with the generated HTML chunks, we open a brand new file called `portfolio.html` in "write" mode (`"w"`) and save our completed website!
