import os
from flask import Flask, render_template, request
from flask_dropzone import Dropzone

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config.update(
    UPLOADED_PATH=os.path.join(basedir, 'uploads'),
    # Flask-Dropzone config:
    DROPZONE_ALLOWED_FILE_TYPE='image',
    DROPZONE_MAX_FILE_SIZE=3,
    DROPZONE_MAX_FILES=30,
)

<<<<<<< HEAD
@app.route('/')
def show_index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def do_upload():
    file = request.files['upload_file']
    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    response = make_response(url_for('static', filename='/upload/'+filename, _external=True))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
=======
dropzone = Dropzone(app)


@app.route('/', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        f = request.files.get('file')
        f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
    return render_template('index.html')

>>>>>>> b31630ebd95cc5dad9b75dcee0c6d300708b22c6

if __name__ == '__main__':
    app.run(debug=True)
