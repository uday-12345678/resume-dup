import re

# Canonical skill → possible variations
SKILL_ALIASES = {
    "java": ["java", "JAVA","Java","core java", "java se", "java ee", "jdk"],
    "python": ["python","Python","PYTHON", "python3", "python programming"],
    "c++": ["c++", "cpp", "C++"],
    "data structures": ["data structures", "ds", "dsa"],
    "algorithms": ["algorithms", "algo"],
    "sql": ["sql","SQL","Sql","MySQL", "PostgreSQL", "Oracle SQL","MYSQL"],
    "excel": ["excel", "ms excel", "microsoft excel"],
    "power bi": ["power bi", "powerbi","Power Bi","POWER BI", "power bi desktop","Power BI"],
    "tableau": ["tableau"],
    "html": ["html", "html5"],
    "css": ["css", "css3"],
    "javascript": ["javascript", "js","Java Script","JavaScript"],
    "react": ["react", "reactjs", "react.js","React.js"],
    "node": ["node", "nodejs", "node.js","Node.js"],
    "mongodb": ["mongodb", "mongo db"],
    "machine learning": ["machine learning", "ml"],
    "deep learning": ["deep learning", "dl"],
    "statistics": ["statistics", "statistical analysis"],
    "data analysis": ["data analysis", "data analytics"],
    "git": ["git", "git version control"],
    "tensorflow": ["tensorflow", "tf","TensorFlow"],
    "express": ["express", "expressjs", "express.js","Express.js"],
    "object oriented programming": ["object oriented programming", "oops","OOPS", "object-oriented programming","Object Oriented Programming"]
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
