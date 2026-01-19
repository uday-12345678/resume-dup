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

# Use a temp directory for uploads (serverless-friendly)
app.config["UPLOAD_FOLDER"] = os.environ.get(
    "UPLOAD_FOLDER",
    os.path.join(tempfile.gettempdir(), "uploads")
)

# Ensure uploads folder exists
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def index():

    # 🔹 GET request → show upload page
    if request.method == "GET":
        return render_template(
            "index.html",
            roles=JOB_ROLES.keys()
        )

    # 🔹 POST request → process analysis
    mode = request.form.get("mode", "role")   # role | jd
    file = request.files.get("resume")
    role = request.form.get("role")
    jd_url = request.form.get("jd_url")
    jd_text = request.form.get("jd_text")

    # Resume is mandatory in all modes
    if not file or not file.filename:
        return render_template(
            "index.html",
            roles=JOB_ROLES.keys()
        )

    # Save resume
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(file_path)

    # Extract resume skills
    resume_text = extract_text_from_pdf(file_path)
    resume_skills = extract_skills(resume_text)

    # 🔹 MODE 1: Job Description Mode (NEW)
    if mode == "jd":

        # JD text has higher priority than URL
        if jd_text and jd_text.strip():
            jd_content = jd_text
        elif jd_url and jd_url.strip():
            jd_content = extract_text_from_url(jd_url)
        else:
            return render_template(
                "index.html",
                roles=JOB_ROLES.keys()
            )

        jd_skills = extract_skills(jd_content)
        analysis = analyze_skills(resume_skills, jd_skills)
        analysis["role"] = "Job Description Based Analysis"

    # 🔹 MODE 2: Job Role Mode (UNCHANGED)
    else:
        if not role:
            return render_template(
                "index.html",
                roles=JOB_ROLES.keys()
            )

        role_skills = JOB_ROLES.get(role, [])
        analysis = analyze_skills(resume_skills, role_skills)
        analysis["role"] = role

    # 🔹 Common post-processing (UNCHANGED)
    analysis["roadmap"] = generate_roadmap(
        analysis["missing_skills"]
    )

    analysis["projects"] = recommend_projects(
        analysis["missing_skills"],
        analysis["match_percentage"],
        max_projects=3
    )

    analysis["filename"] = filename
    analysis["input_type"] = (
        "Resume + Job Description"
        if mode == "jd"
        else "Resume + Job Role"
    )

    return render_template(
        "result.html",
        result=analysis
    )


if __name__ == "__main__":
    app.run(debug=True)
