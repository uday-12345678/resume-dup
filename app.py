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

    # 🔹 POST request → analyze resume or JD URL
    file = request.files.get("resume")
    jd_url = request.form.get("jd_url")
    role = request.form.get("role")

    # Role is mandatory
    if not role:
        return render_template(
            "index.html",
            roles=JOB_ROLES.keys()
        )

    # Decide input source
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
        # Neither resume nor JD URL provided
        return render_template(
            "index.html",
            roles=JOB_ROLES.keys()
        )

    # Extract skills from input text
    input_skills = extract_skills(input_text)

    # Analyze against selected role
    role_skills = JOB_ROLES.get(role, [])
    analysis = analyze_skills(input_skills, role_skills)

    # Generate learning roadmap
    analysis["roadmap"] = generate_roadmap(
        analysis["missing_skills"]
    )

    # Recommend projects (only if match < threshold)
    analysis["projects"] = recommend_projects(
        analysis["missing_skills"],
        analysis["match_percentage"],
        max_projects=3
    )

    analysis["role"] = role
    analysis["filename"] = filename
    analysis["input_type"] = "Resume PDF" if filename else "Job Description URL"

    return render_template(
        "result.html",
        result=analysis
    )


if __name__ == "__main__":
    app.run(debug=True)
