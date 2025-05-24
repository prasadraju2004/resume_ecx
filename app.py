from flask import Flask, Response, render_template, request
# Removed json, os, pdfkit imports as they are handled in pdf_renderer now
from flask_pymongo import PyMongo

# Import your renderers
from renderers.html_renderer import render_html_resume
from renderers.cv_renderer import cv_render
from renderers.pdf_renderer import download_pdf_document # Import the refactored function

app = Flask(__name__)

# MongoDB configuration
app.config["MONGO_URI"] = "mongodb+srv://raju:ecxraju@ecxrb.xyf1gi2.mongodb.net/resume_gen" # Use env variables in production!
mongo = PyMongo(app)

@app.route('/')
def hello_world():
    return '''
        <h1>Resume/CV Generator</h1>
        <h2>View HTML:</h2>
        <p><a href="/render?username=Raju&template=harvard.html">View Raju's Resume (Harvard Template)</a></p>
        <p><a href="/render?username=Raju&template=resume2.html">View Raju's Resume (Resume2 Template)</a></p>
        <p><a href="/cv_render?username=Raju&template=college_template_1.html">View Raju's CV (College Template 1)</a></p>
        <hr>
        <h2>Download PDF:</h2>
        <p><a href="/download?doc_type=resume&username=Raju&template=harvard.html">Download Raju's Resume PDF (Harvard)</a></p>
        <p><a href="/download?doc_type=resume&username=Raju&template=resume2.html">Download Raju's Resume PDF (Resume2)</a></p>
        <p><a href="/download?doc_type=cv&username=Raju&template=college_template_1.html">Download Raju's CV PDF (College Template 1)</a></p>
        <hr>
        <p><i>You can change the 'username' and 'template' parameters in the URL.</i></p>
    '''

# Endpoint to render RESUME HTML
@app.route('/render')
def render_resume_endpoint():
    username = request.args.get('username', 'Raju')
    template = request.args.get('template', 'harvard.html') 
    return render_html_resume(mongo, username=username, template=template)

# Endpoint to render CV HTML
@app.route('/cv_render')
def render_cv_endpoint():
    username = request.args.get('username', 'Raju')
    template = request.args.get('template', 'college_template_1.html') # Default CV template
    return cv_render(mongo, username=username, template=template)

# Endpoint to download CV/Resume as PDF
@app.route('/download')
def download_document_endpoint():
    username = request.args.get('username', 'Raju')
    doc_type = request.args.get('doc_type') 
    template = request.args.get('template') 

    if not doc_type:
        return "Missing required parameter: 'doc_type' (must be 'resume' or 'cv')", 400
    if not template:

        if doc_type == 'resume':
            template = 'harvard.html'
        elif doc_type == 'cv':
            template = 'college_template_1.html' 
        else:
             return f"Invalid 'doc_type': {doc_type}. Use 'resume' or 'cv'.", 400

        app.logger.warning(f"Template not specified for {doc_type}, defaulting to {template}")

    # Call the unified PDF download function
    return download_pdf_document(
        mongo=mongo,
        doc_type=doc_type,
        username=username,
        template=template
    )




if __name__ == '__main__':
    # Set debug=True for development, False for production
    # Use a proper WSGI server (like Gunicorn or Waitress) in production
    app.run(debug=True)