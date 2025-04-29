from flask import render_template, Response
import logging
import pdfkit
import json
import os
import platform

logger = logging.getLogger(__name__)
RESUME_TEMPLATE = 'resume2.html'

# Determine wkhtmltopdf path based on OS
if platform.system() == 'Windows':
    # Local development path (adjust if needed)
    path_wkhtmltopdf = r'D:\software installations data\wkhtmltopdf\bin\wkhtmltopdf.exe'
else:
    # Assume the binary is included in the "bin" directory of the project (Render deployment)
    path_wkhtmltopdf = os.path.join(os.getcwd(), 'bin', 'wkhtmltopdf')

# Configure pdfkit
if not os.path.exists(path_wkhtmltopdf):
    print(f"ERROR: wkhtmltopdf executable not found at: {path_wkhtmltopdf}")
    config = None
else:
    print(f"Using wkhtmltopdf at: {path_wkhtmltopdf}")
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

def download_pdf_resume(mongo):
    """Generates and serves the resume as a PDF file using pdfkit."""

    if config is None:
        return ("<h1>Configuration Error</h1>"
                "<p>wkhtmltopdf path configured does not exist or is incorrect.</p>"), 500

    try:
        # Fetch user data
        user = mongo.db.users.find_one({"username": "Raju"})
        if not user:
            return "User not found", 404

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

        # Render HTML from template
        html_string = render_template(RESUME_TEMPLATE, **context)

        # PDF generation options
        options = {
            'page-size': 'Letter',
            'margin-top': '0.5in',
            'margin-right': '0.5in',
            'margin-bottom': '0.5in',
            'margin-left': '0.5in',
            'encoding': "UTF-8",
            'enable-local-file-access': None,
            'no-outline': None
        }

        # Generate PDF bytes
        pdf_bytes = pdfkit.from_string(
            html_string,
            output_path=False,
            options=options,
            configuration=config
        )

        response = Response(pdf_bytes)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename="resume.pdf"'

        return response

    except FileNotFoundError as e:
        logger.error(f"wkhtmltopdf execution error: {e}")
        return (f"<h1>Error Generating PDF</h1><p>{str(e)}</p>"), 500
    except Exception as e:
        logger.error(f"Unexpected PDF generation error: {e}")
        return (f"<h1>Error Generating PDF</h1><p>{str(e)}</p>"), 500
