import os
from flask import *
from flask_dropzone import Dropzone
from cookme.ReceiptCook import ReadOrderThing

img = Blueprint('img', __name__)
basedir = os.path.abspath(os.path.dirname(__file__)) #ディレクトリ名を取得

app = Flask(__name__)

with app.app_context():
    current_app.config.update(
        UPLOADED_PATH=os.path.join(basedir, ''), #絶対パス
        # Flask-Dropzone config:
        DROPZONE_ALLOWED_FILE_TYPE='image',
        DROPZONE_MAX_FILE_SIZE=3,
        DROPZONE_MAX_FILES=30,
    )

    dropzone = Dropzone(current_app)

@img.route('/upload/<userID>', methods=['POST'])
def upload(userID):
    #if request.method == 'GET':
        #return render_template('index.html')

    f = request.files['file']
    with app.app_context():
        f.save(os.path.join(current_app.config['UPLOADED_PATH'], f.filename))
        return redirect(url_for('img.SearchOrderThing', userID=userID, 
            fileName=f.filename))

@img.route('/SearchOrderThing/<userID>/<fileName>', methods=['GET', 'POST'])
def SearchOrderThing(userID, fileName):
    search_words = ReadOrderThing(fileName)
    return render_template('SearchOrderThing.html', userID=userID,
        OrderThings=search_words)




    
    
