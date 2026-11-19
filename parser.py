"""Resume text extraction and lightweight candidate information parsing."""
import re
from pathlib import Path



SKILLS = [
    "python", "java", "c", "c++", "c#", "javascript", "typescript", "html", "css",
    "sql", "mysql", "postgresql", "mongodb", "flask", "django", "fastapi", "react",
    "node.js", "git", "github", "machine learning", "deep learning", "nlp", "data analysis",
    "pandas", "numpy", "tensorflow", "pytorch", "excel", "power bi", "aws", "docker",
    "linux", "communication", "leadership", "problem solving"
]

EDUCATION_TERMS = ["b.tech", "btech", "b.e", "be ", "m.tech", "mtech", "m.sc", "msc", "b.sc", "bsc", "mba", "bachelor", "master", " diploma", "phd", "school", "college", "university"]


def extract_pdf_text(file_path: str) -> str:
    """Extract text from a PDF file with pdfplumber."""
    import pdfplumber
    text_parts = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text_parts.append(page.extract_text() or "")
    return "\n".join(text_parts).strip()



def parse_resume_text(text: str) -> dict:
    """Extract basic fields from resume text. This is a heuristic demo, not a hiring model."""
    cleaned = re.sub(r"\s+", " ", text).strip()
    email_match = re.search(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", cleaned, re.I)
    phone_match = re.search(r"(?:\+?\d[\d\s().-]{7,}\d)", cleaned)
    found_skills = [skill for skill in SKILLS if re.search(r"(?<![\w])" + re.escape(skill) + r"(?![\w])", cleaned, re.I)]
    education_lines = []
    for line in text.splitlines():
        line_clean = line.strip()
        if line_clean and any(term in line_clean.lower() for term in EDUCATION_TERMS):
            education_lines.append(line_clean[:220])
    # Simple first-line name heuristic; avoids lines that look like contact details or headings.
    name = "Not detected"
    for line in text.splitlines()[:8]:
        candidate = line.strip()
        if (2 <= len(candidate.split()) <= 4 and len(candidate) <= 60
                and not re.search(r"@|\d|resume|curriculum|profile|objective|summary", candidate, re.I)):
            name = candidate
            break
    return {
        "name": name,
        "email": email_match.group(0) if email_match else "Not detected",
        "phone": phone_match.group(0).strip() if phone_match else "Not detected",
        "skills": found_skills,
        "education": education_lines[:8],
        "resume_text": text[:20000],
    }
