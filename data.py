from flask import Flask
from flask_pymongo import PyMongo
from bson import ObjectId
import random
import datetime

app = Flask(__name__)

# MongoDB configuration
app.config["MONGO_URI"] = "mongodb+srv://raju:ecxraju@ecxrb.xyf1gi2.mongodb.net/resume_gen"
mongo = PyMongo(app)

# Sample data
users = [
    {"username": "Ashraf", "mail": "ashraf@example.com", "password": "password123"},
    {"username": "Raju", "mail": "raju@example.com", "password": "password123"},
    {"username": "Prasad", "mail": "prasad@example.com", "password": "password123"},
    {"username": "Baig", "mail": "baig@example.com", "password": "password123"},
    {"username": "Masthan", "mail": "masthan@example.com", "password": "password123"},
]

user_details = [
    {"profile_pic": "profile_pic_url_1", "phn_no": 1234567890, "location": "City A", "linkedin": "linkedin.com/in/ashraf", "github": "github.com/ashraf", "portfolio": "portfolio.com/ashraf", "skills": ["Python", "Flask"], "interests": ["Coding", "Reading"], "field": "Software Development"},
    {"profile_pic": "profile_pic_url_2", "phn_no": 2345678901, "location": "City B", "linkedin": "linkedin.com/in/raju", "github": "github.com/raju", "portfolio": "portfolio.com/raju", "skills": ["Java", "Spring"], "interests": ["Gaming", "Traveling"], "field": "Software Engineering"},
    {"profile_pic": "profile_pic_url_3", "phn_no": 3456789012, "location": "City C", "linkedin": "linkedin.com/in/prasad", "github": "github.com/prasad", "portfolio": "portfolio.com/prasad", "skills": ["JavaScript", "React"], "interests": ["Music", "Sports"], "field": "Web Development"},
    {"profile_pic": "profile_pic_url_4", "phn_no": 4567890123, "location": "City D", "linkedin": "linkedin.com/in/baig", "github": "github.com/baig", "portfolio": "portfolio.com/baig", "skills": ["C++", "Qt"], "interests": ["Photography", "Hiking"], "field": "Game Development"},
    {"profile_pic": "profile_pic_url_5", "phn_no": 5678901234, "location": "City E", "linkedin": "linkedin.com/in/masthan", "github": "github.com/masthan", "portfolio": "portfolio.com/masthan", "skills": ["Ruby", "Rails"], "interests": ["Cooking", "Writing"], "field": "Backend Development"},
]

educations = [
    {"institute_name": "University A", "qualification": "Bachelor's", "specialization": "Computer Science", "year": 2020, "details": "Graduated with honors", "location": "City A"},
    {"institute_name": "University B", "qualification": "Master's", "specialization": "Software Engineering", "year": 2022, "details": "Completed with distinction", "location": "City B"},
    {"institute_name": "University C", "qualification": "Bachelor's", "specialization": "Information Technology", "year": 2019, "details": "Graduated with a GPA of 3.8", "location": "City C"},
    {"institute_name": "University D", "qualification": "Diploma", "specialization": "Game Development", "year": 2021, "details": "Completed with a project on game design", "location": "City D"},
    {"institute_name": "University E", "qualification": "Bachelor's", "specialization": "Web Development", "year": 2020, "details": "Focused on full-stack development", "location": "City E"},
]

experiences = [
    {"company": "Company A", "location": "City A", "title": "Software Engineer", "year": 2021, "description": "Worked on developing web applications."},
    {"company": "Company B", "location": "City B", "title": "Backend Developer", "year": 2022, "description": "Responsible for server-side logic."},
    {"company": "Company C", "location": "City C", "title": "Frontend Developer", "year": 2020, "description": "Developed user interfaces."},
    {"company": "Company D", "location": "City D", "title": "Game Developer", "year": 2021, "description": "Worked on game mechanics."},
    {"company": "Company E", "location": "City E", "title": "Web Developer", "year": 2022, "description": "Created responsive websites."},
]

projects = [
    {"project_name": "Project A", "link": "project_a_link", "title": "Web App", "description": "A web application for task management.", "tech": ["Flask", "MongoDB"]},
    {"project_name": "Project B", "link": "project_b_link", "title": "Game", "description": "A 2D game built using Unity.", "tech": ["Unity", "C#"]},
    {"project_name": "Project C", "link": "project_c_link", "title": "Portfolio", "description": "Personal portfolio website.", "tech": ["HTML", "CSS", "JavaScript"]},
    {"project_name": "Project D", "link": "project_d_link", "title": "API", "description": "RESTful API for a mobile app.", "tech": ["Node.js", "Express"]},
    {"project_name": "Project E", "link": "project_e_link", "title": "E-commerce Site", "description": "An online store built with Django.", "tech": ["Django", "Python"]},
]

awards = [
    {"title": "Best Developer", "year": 2021, "issuer": "Tech Conference"},
    {"title": "Employee of the Month", "year": 2022, "issuer": "Company A"},
    {"title": "Hackathon Winner", "year": 2020, "issuer": "University A"},
    {"title": "Outstanding Project", "year": 2021, "issuer": "Company B"},
    {"title": "Best Innovation", "year": 2022, "issuer": "Tech Summit"},
]

@app.route('/insert_data')
def insert_data():
    # Insert users
    user_ids = []
    for user in users:
        result = mongo.db.users.insert_one(user)
        user_ids.append(result.inserted_id)

    # Insert user details
    for i, user_detail in enumerate(user_details):
        user_detail['user_id'] = user_ids[i]
        mongo.db.user_details.insert_one(user_detail)

    # Insert education
    for i, education in enumerate(educations):
        education['user_id'] = user_ids[i]
        mongo.db.education.insert_one(education)

    # Insert experience
    for i, experience in enumerate(experiences):
        experience['user_id'] = user_ids[i]
        mongo.db.experience.insert_one(experience)

    # Insert projects
    for i, project in enumerate(projects):
        project['user_id'] = user_ids[i]
        mongo.db.projects.insert_one(project)

    # Insert awards
    for i, award in enumerate(awards):
        award['user_id'] = user_ids[i % len(user_ids)]  # Distribute awards among users
        mongo.db.awards.insert_one(award)

    return "Data inserted successfully!"

if __name__ == '__main__':
    app.run(debug=True)