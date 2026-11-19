from pathlib import Path
import os
from flask import Flask, flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename
from parser import extract_pdf_text, parse_resume_text
from database import init_db, add_candidate, search_candidates, get_candidate


BASE_DIR = Path(__file__).parent
UPLOAD_FOLDER = BASE_DIR / "uploads"
UPLOAD_FOLDER.mkdir(exist_ok=True)
ALLOWED_EXTENSIONS = {"pdf"}
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "resume-parser-demo-secret")
app.config["UPLOAD_FOLDER"] = str(UPLOAD_FOLDER)
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024
init_db()



def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route("/", methods=["GET"])
def index():
    query = request.args.get("q", "")
    candidates = search_candidates(query)
    return render_template("index.html", candidates=candidates, query=query)



@app.route("/upload", methods=["POST"])
def upload_resume():
    uploaded = request.files.get("resume")
    if not uploaded or not uploaded.filename:
        flash("Choose a PDF resume to upload.", "error")
        return redirect(url_for("index"))
    if not allowed_file(uploaded.filename):
        flash("Only PDF files are supported in this demo.", "error")
        return redirect(url_for("index"))
    filename = secure_filename(uploaded.filename)
    path = UPLOAD_FOLDER / filename
    uploaded.save(path)
    try:
        text = extract_pdf_text(str(path))
        if not text:
            flash("No readable text was found. Try a text-based PDF instead of a scanned image.", "error")
            return redirect(url_for("index"))
        parsed = parse_resume_text(text)
        candidate_id = add_candidate(parsed, filename)
        flash("Resume parsed and saved successfully.", "success")
        return redirect(url_for("candidate_detail", candidate_id=candidate_id))
    except Exception as exc:
        flash(f"Could not parse this PDF: {exc}", "error")
        return redirect(url_for("index"))
    finally:
        try:
            path.unlink(missing_ok=True)
        except OSError:
            pass



@app.route("/candidate/<int:candidate_id>")
def candidate_detail(candidate_id):
    candidate = get_candidate(candidate_id)
    if not candidate:
        flash("Candidate record not found.", "error")
        return redirect(url_for("index"))
    return render_template("candidate.html", candidate=candidate)



if __name__ == "__main__":
    app.run(debug=True)
