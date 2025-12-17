from flask import Flask, render_template, request
import os
import tempfile
from werkzeug.utils import secure_filename

from resume_parser import extract_text_from_pdf
from skill_extractor import extract_skills
from job_roles import JOB_ROLES
from analyzer import analyze_skills
from roadmap_generator import generate_roadmap
from project_recommender import recommend_projects

app = Flask(__name__)

# Use a temp directory for uploads (serverless-friendly)
app.config["UPLOAD_FOLDER"] = os.environ.get(
    "UPLOAD_FOLDER",
    os.path.join(tempfile.gettempdir(), "uploads")
)

# Ensure uploads folder exists
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def index():
    # 👉 GET request → show upload page
    if request.method == "GET":
        return render_template(
            "index.html",
            roles=JOB_ROLES.keys()
        )

    # 👉 POST request → analyze resume and show result page
    file = request.files.get("resume")
    role = request.form.get("role")

    if not file or not role or not file.filename:
        # Safety fallback
        return render_template(
            "index.html",
            roles=JOB_ROLES.keys()
        )

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(file_path)

    # Resume processing
    resume_text = extract_text_from_pdf(file_path)
    resume_skills = extract_skills(resume_text)

    role_skills = JOB_ROLES.get(role, [])
    analysis = analyze_skills(resume_skills, role_skills)

    # Learning roadmap
    analysis["roadmap"] = generate_roadmap(
        analysis["missing_skills"]
    )

    # Project recommendations (only if match < threshold)
    analysis["projects"] = recommend_projects(
        analysis["missing_skills"],
        analysis["match_percentage"],
        max_projects=3
    )

    analysis["role"] = role
    analysis["filename"] = filename

    return render_template(
        "result.html",
        result=analysis
    )


if __name__ == "__main__":
    app.run(debug=True)
