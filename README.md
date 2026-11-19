# Automated Resume Parser

A beginner-friendly resume parsing web application built with Python and Flask. Upload a text-based PDF resume to extract contact information, skills, education-related lines, and a text preview. Parsed candidate records are stored in SQLite and can be searched from the dashboard.


## Features
- PDF resume upload (10 MB maximum)
- Text extraction with PDFPlumber
- Basic candidate name, email and phone detection
- Keyword-based skills detection
- Education-related line detection
- Candidate database using SQLite
- Search records by name, email, phone, skills or education
- Responsive dashboard and candidate profile view


## Technology stack
- Python
- Flask
- PDFPlumber
- SQLite
- HTML and CSS
- spaCy listed as an NLP dependency for future enhancement; current extraction uses lightweight rules and patterns


## Project structure
```text
Automated-Resume-Parser/
├── app.py
├── parser.py
├── database.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
├── templates/
│   ├── index.html
│   └── candidate.html
└── static/
    └── style.css
```

## Run locally
1. Clone this repository or download the ZIP.
2. Open a terminal in the project directory.
3. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # macOS/Linux
   # venv\\Scripts\\activate  # Windows
   ```
4. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
5. Start the Flask app:
   ```bash
   python app.py
   ```
6. Open http://127.0.0.1:5000 in your browser.

## How it works
1. The user uploads a PDF resume through the web form.
2. PDFPlumber extracts text from the document.
3. The parser identifies email, phone, a best-effort name, skills from a keyword list, and lines likely related to education.
4. The extracted fields and text preview are saved in a local SQLite database.
5. Candidate profiles can be viewed and searched from the dashboard.

## Limitations
- This is a portfolio/demo parser, not a production hiring system.
- Extraction is heuristic and may miss fields or produce false matches. Candidate details should be checked against the source resume.
- Scanned/image-only PDFs are not OCR processed; use text-based PDFs.
- Name and education extraction are approximate.
- The app is designed for local demonstration. Do not upload real resumes or sensitive personal data to a public demo without appropriate consent, security and retention controls.
- spaCy is included as a dependency for possible NLP expansion; a trained spaCy model is not required by the current implementation.

## Future improvements
- OCR for scanned documents
- More robust named-entity extraction with a trained NLP model
- Skill categories and configurable skill dictionary
- Export candidate profiles to CSV
- Duplicate candidate detection
- Authentication, access controls, and secure retention policies

## License
MIT
