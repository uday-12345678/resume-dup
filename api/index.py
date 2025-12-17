from flask import Flask, render_template, request
import os
import tempfile
from werkzeug.utils import secure_filename

from resume_parser import extract_text_from_pdf
from jd_extractor import extract_text_from_url
from skill_extractor import extract_skills
from job_roles import JOB_ROLES
from analyzer import analyze_skills
from roadmap_generator import generate_roadmap
from project_recommender import recommend_projects

app = Flask(__name__)

# Upload directory (serverless safe)
app.config["UPLOAD_FOLDER"] = os.environ.get(
    "UPLOAD_FOLDER",
    os.path.join(tempfile.gettempdir(), "uploads")
)
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template(
            "index.html",
            roles=JOB_ROLES.keys()
        )

    file = request.files.get("resume")
    jd_url = request.form.get("jd_url")
    role = request.form.get("role")

    if not role:
        return render_template("index.html", roles=JOB_ROLES.keys())

    input_text = ""
    filename = None

    if file and file.filename:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)
        input_text = extract_text_from_pdf(file_path)

    elif jd_url:
        input_text = extract_text_from_url(jd_url)

    else:
        return render_template("index.html", roles=JOB_ROLES.keys())

    input_skills = extract_skills(input_text)
    role_skills = JOB_ROLES.get(role, [])

    analysis = analyze_skills(input_skills, role_skills)

    analysis["roadmap"] = generate_roadmap(
        analysis["missing_skills"]
    )

    analysis["projects"] = recommend_projects(
        analysis["missing_skills"],
        analysis["match_percentage"],
        max_projects=3
    )

    analysis["role"] = role
    analysis["filename"] = filename
    analysis["input_type"] = "Resume PDF" if filename else "Job Description URL"

    return render_template("result.html", result=analysis)
