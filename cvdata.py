from flask import Flask
from flask_pymongo import PyMongo
import random

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://raju:ecxraju@ecxrb.xyf1gi2.mongodb.net/resume_gen"
mongo = PyMongo(app)

@app.route('/insert_academic_data')
def insert_academic_data():
    # Get user_ids from the DB
    users = list(mongo.db.users.find())
    user_ids = [user["_id"] for user in users]

    # Sample academic CV data
    for user_id in user_ids:
        # Insert multiple research experiences
        for i in range(2):
            mongo.db.research_experience.insert_one({
                "user_id": user_id,
                "position": "Postdoctoral Fellow" if i == 0 else "Research Assistant",
                "department": f"Dept {i+1}",
                "institution": f"Institution {i+1}",
                "location": f"City {chr(65+i)}",
                "start_year": 2018 + i,
                "end_year": 2019 + i,
                "description": [
                    f"Conducted research on Topic {i+1}.",
                    "Published results in high-impact journals."
                ]
            })

        # Insert multiple teaching experiences
        for i in range(2):
            mongo.db.teaching_experience.insert_one({
                "user_id": user_id,
                "role": "Lecturer" if i == 0 else "Teaching Assistant",
                "course_title": f"Course {i+1}",
                "course_number": f"CS10{i+1}",
                "department": "Computer Science",
                "institution": f"University {i+1}",
                "level": "Undergraduate" if i == 0 else "Graduate",
                "year": 2020 + i,
                "description": f"Taught students fundamental concepts of subject {i+1}."
            })

        # Insert multiple grants
        for i in range(2):
            mongo.db.grants.insert_one({
                "user_id": user_id,
                "grant_title": f"Research Grant {i+1}",
                "amount": 10000 * (i+1),
                "status": "Accepted" if i % 2 == 0 else "Declined",
                "year": 2020 + i,
                "description": f"Funding to explore advanced techniques in Area {i+1}."
            })

        # Insert professional memberships
        mongo.db.professional_memberships.insert_many([
            {
                "user_id": user_id,
                "organization": "ACM",
                "start_year": 2019,
                "end_year": 2024,
                "position": "Member",
                "contributions": ["Reviewed conference papers", "Organized workshops"]
            },
            {
                "user_id": user_id,
                "organization": "IEEE",
                "start_year": 2021,
                "end_year": 2023,
                "position": "Chair",
                "contributions": ["Led technical committee", "Hosted webinars"]
            }
        ])

        # Insert community service
        mongo.db.community_service.insert_many([
            {
                "user_id": user_id,
                "activity": "STEM Outreach",
                "organization": "Local High School",
                "location": "City X",
                "year": 2021,
                "description": "Mentored students in science fair projects."
            },
            {
                "user_id": user_id,
                "activity": "University Committee",
                "organization": "XYZ University",
                "location": "City Y",
                "year": 2022,
                "description": "Served on curriculum review committee."
            }
        ])

        # Insert publications
        for i in range(2):
            mongo.db.publications.insert_one({
                "user_id": user_id,
                "title": f"Publication Title {i+1}",
                "authors": f"User {user_id}, Co-author",
                "publication_type": "Journal" if i % 2 == 0 else "Conference",
                "journal_name": f"Journal/Conference {i+1}",
                "status": "Published" if i % 2 == 0 else "Under Review",
                "year": 2021 + i,
                "link": f"https://example.com/publication{i+1}"
            })

        # Insert references
        mongo.db.references.insert_many([
            {
                "user_id": user_id,
                "name": f"Prof. Ref{i+1}",
                "title": "Professor of AI",
                "affiliation": "Institute of Tech",
                "email": f"ref{i+1}@example.com",
                "phone": "9876543210",
                "relation": "PhD Supervisor"
            } for i in range(2)
        ])

    return "Academic CV data inserted successfully!"

if __name__ == '__main__':
    app.run(debug=True)
