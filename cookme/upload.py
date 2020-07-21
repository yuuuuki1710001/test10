"""
    upload  :   レシート画像をアップロードする
    Date    :   2020/07/21
    purpose :   レシート画像をアップロードする
"""



import os
from flask import *
from flask_dropzone import Dropzone
from cookme.ReceiptCook import readOrderThing

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




"""
    FunctionName    :   upload
    Data            :   2020/07/21
    Designer        :   野田啓介
    Function        :   レシート画像をアップロードする
    Entry           :   userID   --- ユーザー名
    Return          :   SearchOrderThingメソッドにリダイレクトする
                        userID   --- ユーザー名
                        fileName --- レシート画像のファイル名
"""
@img.route('/upload/<userID>', methods=['GET', 'POST'])
def upload(userID):
    #if request.method == 'GET':
        #return render_template('index.html')

    f = request.files.get('file')

    with app.app_context():
        try:
            f.save(os.path.join(current_app.config['UPLOADED_PATH'], f.filename))


        #except FileNotFoundError:
            #flash('アップロードするファイルを選んでください', 'failed')
            #return redirect(url_for('cookme.Home', userID=userID))

        except IsADirectoryError:
            flash('アップロードするファイルを選んでください', 'failed')
            return redirect(url_for('cookme.home', userID=userID))

        return redirect(url_for('img.searchOrderThing', userID=userID, 
            fileName=f.filename))



"""
    FunctionName    :   SearchOrderThing
    Data            :   2020/07/21
    Designer        :   野田啓介
    Function        :   ホーム画面表示
    Entry           :   userID      --- ユーザー名
                        fileName    --- レシート画像のファイル名
    Return          :   ホーム画面に遷移
                        userID      --- ユーザー名
                        searchWords --- レシート画像から読み込まれた材料(list型)
"""
@img.route('/SearchOrderThing/<userID>/<fileName>', methods=['GET', 'POST'])
def searchOrderThing(userID, fileName):

    if fileName.count(' ') >= 1:
        flash('ファイル名に空白スペースがあります', 'message')
        return redirect(url_for('cookme.Home', userID=userID))

    if fileName.count('.') >= 2:
        flash('ファイル名にドット(.)が2つ以上あります', 'message')
        return redirect(url_for('cookme.Home', userID=userID))
    
    if '.jpg' in fileName:
        searchWords = readOrderThing(fileName)

        #材料を読み込んだらファイルを削除
        fileName = fileName.replace('.jpg', '')
        os.remove('cookme/{}.jpg'.format(fileName))

    elif '.jpeg' in fileName:
        searchWords = readOrderThing(fileName)

        #材料を読み込んだらファイルを削除
        fileName = fileName.replace('.jpeg', '')
        os.remove('cookme/{}.jpeg'.format(fileName))

    elif '.JPG' in fileName:
        searchWords = readOrderThing(fileName)

        #材料を読み込んだらファイルを削除
        fileName = fileName.replace('.JPG', '')
        os.remove('cookme/{}.JPG'.format(fileName))
    
    elif '.png' in fileName:
        searchWords = readOrderThing(fileName)

        #材料を読み込んだらファイルを削除
        fileName = fileName.replace('.png', '')
        os.remove('cookme/{}.png'.format(fileName))

    elif '.PNG' in fileName:
        searchWords = readOrderThing(fileName)

        #材料を読み込んだらファイルを削除
        fileName = fileName.replace('.PNG', '')
        os.remove('cookme/{}.PNG'.format(fileName))

    else:
        flash('拡張子が違います', 'failed')
        return redirect(url_for('cookme.home', userID=userID))


    #ファイルを削除
    
    if os.path.exists('cookme/{}_drawcont.jpg'.format(fileName)) == True:
        os.remove('cookme/{}_drawcont.jpg'.format(fileName))
    
    if os.path.exists('cookme/{}_gray.jpg'.format(fileName)) == True:
        os.remove('cookme/{}_gray.jpg'.format(fileName))

    if os.path.exists('cookme/{}_rect_th.jpg'.format(fileName)) == True:
        os.remove('cookme/{}_rect_th.jpg'.format(fileName))

    if os.path.exists('cookme/{}_th.jpg'.format(fileName)) == True:
        os.remove('cookme/{}_th.jpg'.format(fileName))
    

    return render_template('SearchOrderThing.html', userID=userID,
        orderThings=searchWords)




    
    
