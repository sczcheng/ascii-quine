from pickle import TRUE
from markupsafe import escape 
import imghdr
import os
from flask import Flask, render_template, request, redirect, url_for, abort, \
    send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('home.html')

@app.route('/upload')
def upload_pic():
    return render_template('upload_pic.html')


@app.route('/rendered', methods=['POST'])
def picture_render():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        filename = secure_filename(uploaded_file.filename)
    else:
        filename='boop'
    os.makedirs("uploads",exist_ok=True)
    uploaded_file.save(os.path.join("uploads",filename))
    #santifunction(filename)
    return render_template('rendered.html', santi='blah blah blah')