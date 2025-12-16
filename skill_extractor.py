import re

# Canonical skill → possible variations
SKILL_ALIASES = {
    "java": ["java", "core java", "java se", "java ee", "jdk"],
    "python": ["python", "python3", "python programming"],
    "c++": ["c++", "cpp"],
    "data structures": ["data structures", "ds", "dsa"],
    "algorithms": ["algorithms", "algo"],
    "sql": ["sql", "mysql", "postgresql", "oracle sql"],
    "excel": ["excel", "ms excel", "microsoft excel","Excel"],
    "power bi": ["power bi", "powerbi","Power Bi"],
    "tableau": ["tableau"],
    "html": ["html", "html5","HTML"],
    "css": ["css", "css3","CSS"],
    "javascript": ["javascript", "js","Java Script"],
    "react": ["react", "reactjs","react.js","React.js"],
    "node": ["node", "nodejs","node.js","Node.js"],
    "mongodb": ["mongodb", "mongo db"],
    "machine learning": ["machine learning", "ml","Machine Learning"],
    "deep learning": ["deep learning", "dl"],
    "statistics": ["statistics", "statistical analysis"],
    "data analysis": ["data analysis", "data analytics"],
    "git": ["git", "git version control"],
    "express": ["express", "expressjs", "express.js","Express.js"]
}

def extract_skills(text):
    text = text.lower()
    found_skills = []

    for skill, aliases in SKILL_ALIASES.items():
        for alias in aliases:
            # word boundary avoids partial matches
            if re.search(r"\b" + re.escape(alias) + r"\b", text):
                found_skills.append(skill)
                break

    return list(set(found_skills))

