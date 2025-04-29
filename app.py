from flask import Flask, Response, render_template,request
import json
import os
import pdfkit
from flask_pymongo import PyMongo
from renderers.html_renderer import render_html_resume
from renderers.pdf_renderer import download_pdf_resume
from renderers.cv_renderer import cv_render

app = Flask(__name__)

# MongoDB configuration
app.config["MONGO_URI"] = "mongodb+srv://raju:ecxraju@ecxrb.xyf1gi2.mongodb.net/resume_gen"
mongo = PyMongo(app)

RESUME_TEMPLATE = 'resume2.html'



@app.route('/')
def hello_world():
    return '''
        <h1>Resume Generator</h1>
        <p><a href="/render?username=Raju&template=harvard.html">View Resume HTML</a></p>
        <p><a href="/download-pdf">Download Resume as PDF (using pdfkit)</a></p>
        <p><a href="/cv_render?username=Raju&template=college_template_1.html">View CV in HTML</a></p>
    '''

#we have 3 api endpoints now 1.) render resume, 2.) download pdf, 3.) cv render
#we furthur need code to download the pdf of rendered CV
#127.0.0.1:5000/render?username=""
#127.0.0.1:5000/download?username=""
#127.0.0.1:5000/cv_render?username=""

@app.route('/render')
def render_resume():
    username = request.args.get('username', 'Raju')  # default 'Raju'
    template = request.args.get('template', 'harvard.html')  # default 'harvard.html'
    return render_html_resume(mongo, username=username, template=template)

@app.route('/download-pdf')
def download_resume():
   return download_pdf_resume(mongo)

@app.route('/cv_render')
def render_CV():
    username = request.args.get('username', 'Raju')  # default 'Raju'
    template = request.args.get('template', 'college_template_1.html')  # default 'college_template_1.html'
    return cv_render(mongo, username=username, template=template)



if __name__ == '__main__':
    app.run()