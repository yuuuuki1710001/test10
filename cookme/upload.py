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

@img.route('/upload/<userID>', methods=['GET', 'POST'])
def upload(userID):
    #if request.method == 'GET':
        #return render_template('index.html')

    f = request.files.get('file')

    with app.app_context():
        try:
            f.save(os.path.join(current_app.config['UPLOADED_PATH'], f.filename))

        except FileNotFoundError:
            flash('アップロードするファイルを選んでください', 'message')
            return redirect(url_for('cookme.Home', userID=userID))
            
        return redirect(url_for('img.SearchOrderThing', userID=userID, 
            fileName=f.filename))

@img.route('/SearchOrderThing/<userID>/<fileName>', methods=['GET', 'POST'])
def SearchOrderThing(userID, fileName):
    
    if '.jpg' in fileName:
        search_words = ReadOrderThing(fileName)

        #材料を読み込んだらファイルを削除
        fileName = fileName.replace('.jpg', '')
        os.remove('cookme/{}.jpg'.format(fileName))

    elif '.jpeg' in fileName:
        search_words = ReadOrderThing(fileName)

        #材料を読み込んだらファイルを削除
        fileName = fileName.replace('.jpeg', '')
        os.remove('cookme/{}.jpeg'.format(fileName))

    elif '.JPG' in fileName:
        search_words = ReadOrderThing(fileName)

        #材料を読み込んだらファイルを削除
        fileName = fileName.replace('.JPG', '')
        os.remove('cookme/{}.JPG'.format(fileName))
    
    elif '.png' in fileName:
        search_words = ReadOrderThing(fileName)

        #材料を読み込んだらファイルを削除
        fileName = fileName.replace('.png', '')
        os.remove('cookme/{}.png'.format(fileName))

    elif '.PNG' in fileName:
        search_words = ReadOrderThing(fileName)

        #材料を読み込んだらファイルを削除
        fileName = fileName.replace('.PNG', '')
        os.remove('cookme/{}.PNG'.format(fileName))

    elif '.HEIC' in fileName:
        search_words = ReadOrderThing(fileName)

        #材料を読み込んだらファイルを削除
        fileName = fileName.replace('.HEIC', '')
        os.remove('cookme/{}.HEIC'.format(fileName))

    else:
        flash('拡張子が違います', 'message')
        return redirect(url_for('cookme.Home', userID=userID))


    #ファイルを削除
    os.remove('cookme/{}_drawcont.jpg'.format(fileName))
    os.remove('cookme/{}_gray.jpg'.format(fileName))
    os.remove('cookme/{}_rect_th.jpg'.format(fileName))
    os.remove('cookme/{}_th.jpg'.format(fileName))
    

    return render_template('SearchOrderThing.html', userID=userID,
        OrderThings=search_words)




    
    
