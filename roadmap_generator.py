from learning_roadmap import LEARNING_RESOURCES
from learning_links import LEARNING_LINKS

def generate_roadmap(missing_skills):
    roadmap = []
    week = 1

    for skill in missing_skills:
        description = LEARNING_RESOURCES.get(
            skill,
            "Learn fundamentals and practice projects related to this skill"
        )

        # NEW: fetch learning links for the skill
        links = LEARNING_LINKS.get(skill, {
            "websites": [],
            "youtube": []
        })

        roadmap.append({
            "week": f"Week {week}",
            "skill": skill,
            "description": description,
            "links": links   # ✅ added, no existing logic removed
        })

        week += 1

    return roadmap
