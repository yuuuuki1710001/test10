from flask import Flask, request, url_for, render_template, make_response
import os

SECRET_KEY = 'development key'
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config.from_object(__name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def show_index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def do_upload():
    file = request.files['xhr2upload']
    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    response = make_response(url_for('static', filename='uploads/'+filename, _external=True))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

if __name__ == '__main__':
    app.run(debug = True)