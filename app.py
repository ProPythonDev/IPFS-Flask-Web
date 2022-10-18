from flask import Flask
from flask import render_template, request, redirect
from werkzeug.utils import secure_filename
import ipfsApi
import os
import webbrowser

UPLOAD_FOLDER = r'static\uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_EXTENSIONS'] = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']

@app.route('/')
def home():
    return render_template('upload.html')

@app.route('/uploader', methods = ['POST'])
def upload_file():
    f = request.files['file']
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
    api = ipfsApi.Client('127.0.0.1', 5001)
    res = api.add(f'static\\uploads\\{f.filename}')
    return res

@app.route('/find')
def find():
    return render_template('find.html')

@app.route('/find-ipfs', methods = ['POST'])
def find_to_ipfs():
    fileHash = request.form['text']
    webbrowser.open(f"https://ipfs.io/ipfs/{fileHash}")
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)
