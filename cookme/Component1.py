"""
    C1:UI処理部
    Date:2020/07/05
    purpose:ホーム画面, 検索結果画面, お気に入り登録画面, お気に入り表示画面,
            お気に入り削除画面, 履歴画面, レシピ表示画面を表示する
"""

from flask import *
from werkzeug.exceptions import BadRequestKeyError
import pymysql
from cookme.C3 import CleanWords, IngredientsInputs
from cookme.C4 import selectURL, recipeDisplay
from cookme.FavoriteMain import FavoriteRegister, FavoriteDelete, FavoriteDisplay
from cookme.HistoryMain import HistoryDisplay, HistoryRegister

#MySQLに接続する
conn = pymysql.connect(
                    host='172.30.27.88',
                    user='admin',
                    passwd='10pan',
                    db='cook',
                    port=3306,
                    charset='utf8'
)
cur = conn.cursor()
cur.execute('USE cook')

#app = Flask(__name__)
cookme = Blueprint('cookme', __name__)
#cookme.config['SECRET_KEY'] = 'sample1203'



"""
    FunctionName    :   Home
    Data            :   2020/07/04
    Designer        :   野田啓介
    Function        :   ホーム画面
    Entry           :   userID --- ユーザー名
    Return          :   home.htmlを読み込む
                        userID --- ユーザー名
"""
@cookme.route('/Home/<userID>', methods=['GET', 'POST'])
def Home(userID):
    #userID = request.form['userID']
    return render_template('Home.html', userID=userID) #Home.htmlを読み込む


"""
    FunctionName    :   SearchResult
    Data            :   2020/07/05
    Designer        :   野田啓介
    Function        :   レシピ検索候補主処理
    Entry           :   userID --- ユーザー名
    Return          :   SearchResult.htmlを読み込む
                        userID --- ユーザーID
                        recipeTitles --- 検索候補のレシピタイトル(list型)
"""
@cookme.route('/SearchResult/<userID>', methods=['POST'])
def SearchResult(userID):
    try:
        userID = request.form['userID']                   #ユーザーID
        OrderThing = request.form['OrderThing']           #材料名
    
    #材料名が入力されていないとき
    except BadRequestKeyError:
        OrderThing = ''

    try:
        recipeTime = request.form['recipeTime']           #調理時間

    #調理時間が入力されていないとき
    except BadRequestKeyError:
        recipeTime = -1

    recipeTitles = IngredientsInputs(OrderThing, recipeTime) #レシピの検索候補
    return render_template('SearchResult.html', userID=userID, recipeTitles=recipeTitles) #SearchResult.htmlを読み込む



"""
    FunctionName    :   RecipeDisplay
    Data            :   2020/07/04
    Designer        :   野田啓介
    Function        :   レシピ表示主処理
    Entry           :   userID --- ユーザー名
    Return          :   RecipeDisplay.htmlを読み込む
                        userID       --- ユーザーID
                        recipeTitle  --- レシピタイトル(str型)
                        OrderThing   --- 材料名
                        recipeToCook --- 作り方
"""
@cookme.route('/RecipeDisplay/<userID>', methods=['POST'])
def RecipeDisplay(userID):

    #お気に入りのレシピを削除する
    try:
        recipeTitle = request.form['submit_button'] #お気に入りのレシピタイトル
        return redirect(url_for('cookme.FavoriteDeletion', userID=userID, recipeTitle=recipeTitle)) #FavoriteDeletionメソッドに飛ぶ

    #レシピの内容を取得する
    except BadRequestKeyError:
        recipeTitle = request.form['recipeTitle']                    #レシピタイトル
        print(recipeTitle)
        OrderThing, recipeToCook = recipeDisplay(recipeTitle)        #材料と作り方
        HistoryRegister(userID, selectURL(recipeTitle), recipeTitle) #履歴に格納
        return render_template('RecipeDisplay.html', userID=userID, 
            recipeTitle=recipeTitle, OrderThing=OrderThing, recipeToCook=recipeToCook) #RecipeDisplay.htmlを読み込む



"""
    FunctionName    :   Favorite
    Data            :   2020/07/04
    Designer        :   野田啓介
    Function        :   お気に入り表示処理
    Entry           :   userID       --- ユーザー名
    Return          :   Favorite.htmlを読み込む
                        userID       --- ユーザーID
                        recipeTitles --- お気に入りのレシピタイトル(list型)
"""
@cookme.route('/Favorite/<userID>', methods=['POST'])
def Favorite(userID):
    recipeTitles = FavoriteDisplay(userID) #お気に入りのレシピ一覧
    return render_template('Favorite.html', userID=userID, recipeTitles=recipeTitles) #Favorite.htmlを読み込む



"""
    FunctionName    :   FavoriteRegistration
    Data            :   2020/07/04
    Designer        :   野田啓介
    Function        :   お気に入り登録処理
    Entry           :   userID --- ユーザー名
    Return          :   FavoriteRegistration.htmlを読み込む
"""
@cookme.route('/FavoriteRegistration/<userID>', methods=['POST'])
def FavoriteRegistration(userID):
    recipeTitle = request.form['recipeTitle']                                            #お気に入り登録するレシピタイトル
    cur.execute('SELECT recipeURL FROM cookpages WHERE recipeTitle = %s', (recipeTitle)) #お気に入りレシピのURLを取得

    registerFlag = FavoriteRegister(userID, cur.fetchone()[0], recipeTitle)              #フラグ(0:登録, 1:既に登録されている)

    #お気に入りに登録するとき
    if registerFlag == 0:
        flash('お気に入りに登録しました', 'message')

    #既に登録されているとき
    else:
        flash('既にお気に入りに登録されています', 'message')
    
    return render_template('FavoriteRegistration.html') #FavoriteRegistration.htmlを読み込む



"""
    FunctionName    :   FavoriteDelete
    Data            :   2020/07/04
    Designer        :   野田啓介
    Function        :   お気に入り削除処理
    Entry           :   userID --- ユーザー名
    Return          :   FavoriteDelete.htmlを読み込む
                        userID --- ユーザーID
                        recipeTitles --- 検索候補のレシピタイトル(list型)
"""
@cookme.route('/FavoriteDeletion/<userID>/<recipeTitle>', methods=['GET', 'POST'])
def FavoriteDeletion(userID, recipeTitle):
    FavoriteDelete(userID, recipeTitle) #お気に入りレシピの削除
    flash('削除しました', 'message')
    return render_template('FavoriteDeletion.html', userID=userID, recipeTitle=recipeTitle) #FavoriteDeletion.htmlを読み込む



"""
    FunctionName    :   History
    Data            :   2020/07/04
    Designer        :   野田啓介
    Function        :   履歴処理
    Entry           :   userID --- ユーザー名
    Return          :   SearchResult.htmlを読み込む
                        userID        --- ユーザーID
                        HistoryTitles --- 検索候補のレシピタイトル(list型)
"""
@cookme.route('/History/<userID>', methods=['POST'])
def History(userID):
    historyTitles = HistoryDisplay(userID) #履歴のレシピ一覧
    return render_template('History.html', userID=userID, historyTitles=historyTitles) #History.htmlを読み込む


