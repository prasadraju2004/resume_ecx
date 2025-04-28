from flask import Flask, Response, render_template
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
        <p><a href="/render">View Resume HTML</a></p>
        <p><a href="/download-pdf">Download Resume as PDF (using pdfkit)</a></p>
        <p><a href="/cv_render">View CV in HTML</a></p>
    '''

#we have 3 api endpoints now 1.) render resume, 2.) download pdf, 3.) cv render
#we furthur need code to download the pdf of rendered CV
#127.0.0.1:5000/render?username=""
#127.0.0.1:5000/download?username=""
#127.0.0.1:5000/cv_render?username=""

@app.route('/render')
def render_resume():
    return render_html_resume(mongo)

@app.route('/download-pdf')
def download_resume():
   return download_pdf_resume(mongo)

@app.route('/cv_render')
def render_CV():
    return cv_render(mongo)


if __name__ == '__main__':
    app.run(debug=True)