from flask import render_template, Response

def render_html_resume(mongo, username="Raju", template="harvard.html"):
    # Fetch user by username
    user = mongo.db.users.find_one({"username": username})
    
    if not user:
        return f"User '{username}' not found", 404

    # Fetch user details
    user_details = mongo.db.user_details.find_one({"user_id": user['_id']})
    education = list(mongo.db.education.find({"user_id": user['_id']}))
    experience = list(mongo.db.experience.find({"user_id": user['_id']}))
    projects = list(mongo.db.projects.find({"user_id": user['_id']}))
    awards = list(mongo.db.awards.find({"user_id": user['_id']}))

    context = {
        "name": user['username'],
        "location": user_details.get('location', ''),
        "phone": user_details.get('phn_no', ''),
        "email": user['mail'],
        "linkedin": user_details.get('linkedin', ''),
        "github": user_details.get('github', ''),
        "portfolio": user_details.get('portfolio', ''),
        "summary": user_details.get('summary', ''),
        "education": education,
        "experience": experience,
        "projects": projects,
        "skills": ', '.join(user_details.get('skills', [])),
        "languages": ', '.join(user_details.get('languages', [])),
        "interests": ', '.join(user_details.get('interests', [])),
        "awards": awards,
    }

    return render_template(template, **context)
