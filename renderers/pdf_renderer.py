from flask import render_template, Response
import logging
import pdfkit
import json
import os

logger = logging.getLogger(__name__)
RESUME_TEMPLATE = 'resume2.html'

path_wkhtmltopdf = r'D:\software installations data\wkhtmltopdf\bin\wkhtmltopdf.exe'

# Check if the specified path exists
if not os.path.exists(path_wkhtmltopdf):
    print(f"ERROR: wkhtmltopdf executable not found at the specified path: {path_wkhtmltopdf}")
    print("Please verify the path and ensure wkhtmltopdf is installed correctly.")
    config = None
else:
    print(f"Configuring pdfkit to use wkhtmltopdf at: {path_wkhtmltopdf}")
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

def download_pdf_resume(mongo):
    """Generates and serves the resume as a PDF file using pdfkit."""

    if config is None:
         # Handle the case where the path was invalid during startup
         return ("<h1>Configuration Error</h1>"
                 "<p>wkhtmltopdf path configured in app.py does not exist or is incorrect."
                 "Please verify the path.</p>"), 500

    try:
        # Fetch user details for the user named "Raju"
        user = mongo.db.users.find_one({"username": "Raju"})
        
        if not user:
            return "User not found", 404

        # Fetch user details, education, experience, projects, awards, etc.
        user_details = mongo.db.user_details.find_one({"user_id": user['_id']})
        education = list(mongo.db.education.find({"user_id": user['_id']}))
        experience = list(mongo.db.experience.find({"user_id": user['_id']}))
        projects = list(mongo.db.projects.find({"user_id": user['_id']}))
        awards = list(mongo.db.awards.find({"user_id": user['_id']}))

        # Prepare the context for rendering the template
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

        # Generate the HTML string for the PDF
        html_string = render_template(RESUME_TEMPLATE, **context)

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

        # Generate PDF bytes using the configured path
        pdf_bytes = pdfkit.from_string(
            html_string,
            output_path=False,  # Return bytes
            options=options,
            configuration=config  # Use the specific configuration
        )

        response = Response(pdf_bytes)
        response.headers['Content-Type'] = 'application/pdf'
        filename = "resume.pdf"  # Default filename
        response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'

        return response

    except FileNotFoundError as e:
        logger.error(f"Error executing wkhtmltopdf (check path/permissions): {e}")
        return ("<h1>Error Generating PDF: Execution Failed</h1>"
                "<p>Could not execute wkhtmltopdf found at the configured path. "
                "Please check file permissions and ensure the path is correct.</p>"
                f"<p>Path used: {path_wkhtmltopdf}</p>"), 500
    except Exception as e:
        logger.error(f"Error generating PDF with pdfkit: {e}")
        return f"<h1>Error Generating PDF</h1><p>An unexpected error occurred. Error: {e}</p>", 500
