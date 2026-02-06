import os
import shutil
from datetime import datetime, timedelta
from dotenv import load_dotenv
from exa_py import Exa
from cv_processor import extract_text_from_pdf

load_dotenv()

# Configuration
CV_PATH = "my_cv.pdf"
OUTPUT_DIR = "my_applications"
TARGET_ROLE = "Python Developer"
TARGET_LOCATION = "Remote"

# Initialize APIs
exa_key = os.environ.get("EXA_API_KEY")
if not exa_key:
    print("CRITICAL: EXA_API_KEY not found. Please set it in .env")
    exit(1)
    
exa = Exa(api_key=exa_key)

def generate_cover_letter(cv_text, job_title, job_url, job_date):
    """
    Generates a professional cover letter using a smart template.
    No AI API required.
    """
    
    # Simple extraction of potential company name from domain (heuristic)
    try:
        domain = job_url.split("//")[-1].split("/")[0]
        company_name = domain.replace("www.", "").split(".")[0].title()
    except:
        company_name = "the hiring team"

    # Basic skill matching (check if these exist in CV to emphasize them)
    # This makes the template feel "aware" of the user's actual CV
    cv_lower = cv_text.lower()
    skills_highlight = []
    common_skills = ["python", "django", "flask", "react", "aws", "docker", "sql", "git"]
    
    for skill in common_skills:
        if skill in cv_lower:
            skills_highlight.append(skill.title())
            
    skill_sentence = ""
    if skills_highlight:
        top_3 = ", ".join(skills_highlight[:3])
        skill_sentence = f"With my strong background in {top_3}, I am confident I can hit the ground running."

    today_date = datetime.now().strftime("%B %d, %Y")

    template = f"""{today_date}

Hiring Manager
{company_name}

Re: Application for {job_title} Position

Dear Hiring Manager,

I am writing to express my strong interest in the {job_title} role recently posted on {job_date} (found via {domain}). As a highly motivated developer, I was excited to see an opening at {company_name} that aligns so well with my technical expertise.

{skill_sentence}

In my attached resume, you will find details of my experience in building scalable software solutions. I thrive in collaborative environments and am passionate about writing clean, efficient code. I am particularly eager to bring my problem-solving skills to your team.

Thank you for your time and consideration. I look forward to the possibility of discussing how my skills would add value to {company_name}.

Sincerely,

Enthusiastic Candidate
(See attached CV)
"""
    return template

def run_agent():
    print("--- Job Application Agent (Template Mode) Starting ---")
    
    # 1. Read CV
    if os.path.exists(CV_PATH):
        print(f"Reading CV from {CV_PATH}...")
        cv_text = extract_text_from_pdf(CV_PATH)
        if not cv_text:
            print("Error reading CV content. Proceeding with generic template.")
            cv_text = ""
    else:
        print(f"CV not found at {CV_PATH}. Using generic placeholder skills.")
        cv_text = ""

    # 2. Search Jobs
    print(f"Searching for '{TARGET_ROLE}' jobs...")
    try:
        results = exa.search(
            query=f"Hiring {TARGET_ROLE} in {TARGET_LOCATION} posted recently",
            type="auto",
            num_results=5, 
            start_published_date=(datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        )
    except Exception as e:
        print(f"Search failed: {e}")
        return

    print(f"Found {len(results.results)} jobs. Generating application packages...")
    
    # 3. Create Applications
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)
    
    for i, job in enumerate(results.results, 1):
        # Sanitize folder name
        safe_title = "".join(c for c in job.title if c.isalnum() or c in (' ', '_')).strip()[:30]
        folder_name = f"{i:02d}_{safe_title}"
        folder_path = os.path.join(OUTPUT_DIR, folder_name)
        os.makedirs(folder_path, exist_ok=True)
        
        print(f"[{i}/{len(results.results)}] Generating for: {job.title}")
        
        # Details File
        with open(os.path.join(folder_path, "Job_Details.txt"), "w", encoding="utf-8") as f:
            f.write(f"Title: {job.title}\n")
            f.write(f"URL: {job.url}\n")
            f.write(f"Published: {job.published_date}\n")
            
        # Cover Letter (using template)
        # We handle published_date being possibly None or a string
        pub_date = job.published_date if job.published_date else "recent"
        cl_content = generate_cover_letter(cv_text, job.title, job.url, pub_date)
        
        with open(os.path.join(folder_path, "Cover_Letter.txt"), "w", encoding="utf-8") as f:
            f.write(cl_content)
            
        # Internet Shortcut (.url file for Windows)
        with open(os.path.join(folder_path, "Apply_Link.url"), "w") as f:
            f.write(f"[InternetShortcut]\nURL={job.url}")
            
    print(f"\n✅ Done! Check the '{OUTPUT_DIR}' folder.")

if __name__ == "__main__":
    run_agent()
