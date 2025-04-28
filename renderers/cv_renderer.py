from flask import render_template, Response

RESUME_TEMPLATE = 'college_template_1.html'

def cv_render(mongo, username="Raju"):
    # Fetch user by username
    user = mongo.db.users.find_one({"username": username})
    if not user:
        return f"User '{username}' not found", 404

    user_id = user['_id']

    # Fetch associated collections
    user_details = mongo.db.user_details.find_one({"user_id": user_id})
    education = list(mongo.db.education.find({"user_id": user_id}))
    experience = list(mongo.db.experience.find({"user_id": user_id}))
    projects = list(mongo.db.projects.find({"user_id": user_id}))
    awards = list(mongo.db.awards.find({"user_id": user_id}))
    
    # New Academic CV-specific collections
    research_experience = list(mongo.db.research_experience.find({"user_id": user_id}))
    teaching_experience = list(mongo.db.teaching_experience.find({"user_id": user_id}))
    grants = list(mongo.db.grants.find({"user_id": user_id}))
    professional_memberships = list(mongo.db.professional_memberships.find({"user_id": user_id}))
    community_service = list(mongo.db.community_service.find({"user_id": user_id}))
    publications = list(mongo.db.publications.find({"user_id": user_id}))
    references = list(mongo.db.references.find({"user_id": user_id}))

    # Prepare data for template rendering
    context = {
        "name": user['username'],
        "email": user.get('mail', ''),
        "location": user_details.get('location', ''),
        "phone": user_details.get('phn_no', ''),
        "linkedin": user_details.get('linkedin', ''),
        "github": user_details.get('github', ''),
        "portfolio": user_details.get('portfolio', ''),
        "profile_pic": user_details.get('profile_pic', ''),
        "summary": user_details.get('summary', ''),
        "skills": ', '.join(user_details.get('skills', [])),
        "languages": ', '.join(user_details.get('languages', [])),
        "interests": ', '.join(user_details.get('interests', [])),
        "field": user_details.get('field', ''),
        
        # Existing data
        "education": education,
        "experience": experience,
        "projects": projects,
        "awards": awards,
        
        # Academic CV data
        "research_experience": research_experience,
        "teaching_experience": teaching_experience,
        "grants": grants,
        "professional_memberships": professional_memberships,
        "community_service": community_service,
        "publications": publications,
        "references": references,
    }

    return render_template(RESUME_TEMPLATE, **context)
