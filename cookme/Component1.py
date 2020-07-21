"""
    C1      :   UI処理部
    Date    :   2020/07/21
    purpose :   ホーム画面, 検索結果画面, お気に入り登録画面, お気に入り表示画面,お気に入り削除画面, 履歴画面, レシピ表示画面を表示する
"""

from flask import *
#from flask_bootstrap import Bootstrap
from werkzeug.exceptions import BadRequestKeyError
import pymysql
from cookme.Component3 import ingredientsInputs
from cookme.Component4 import selectURL, RecipeDisplay
from cookme.Component5 import favoriteRegister, favoriteDelete, favoriteDisplay
from cookme.Component6 import historyDisplay, historyRegister

#MySQL接続
conn = pymysql.connect(
    user    =   'root',
    passwd  =   '10pan',
    db      =   'cook',
    port    =   3306,
    charset =   'utf8'
)
cur = conn.cursor()
cur.execute('USE cook')

cookme = Blueprint('cookme', __name__)


"""
    FunctionName    :   home
    Data            :   2020/07/21
    Designer        :   野田啓介
    Function        :   ホーム画面表示
    Entry           :   userID  --- ユーザー名
    Return          :   ホーム画面に遷移
                        userID  --- ユーザー名
"""
@cookme.route('/Home/<userID>', methods=['GET', 'POST'])
def home(userID):
    return render_template('Home.html', userID=userID) #Home.htmlを読み込む
    


"""
    FunctionName    :   searchResult
    Data            :   2020/07/21
    Designer        :   野田啓介
    Function        :   レシピ検索候補画面表示
    Entry           :   userID          --- ユーザー名
    Return          :   レシピ候補画面へ遷移
                        userID          --- ユーザーID
                        recipeTitles    --- 検索候補のレシピタイトル(list型)
"""
@cookme.route('/SearchResult/<userID>', methods=['POST'])
def searchResult(userID):
    orderThing = request.form['orderThing']           #材料名
    recipeTime = request.form['recipeTime']           #調理時間

    #材料名も調理時間も入力されていないとき
    if not orderThing and not recipeTime:
        session.clear()
        flash('材料名か調理時間を入力してください', 'failed')
        return redirect(url_for('cookme.home', userID=userID))

    #材料名が入力されていないとき
    if not orderThing:
        orderThing = ''

    #調理時間が入力されていないとき
    if not recipeTime:
        recipeTime = -1

    recipeTitles = ingredientsInputs(orderThing, recipeTime) #レシピの検索候補
    return render_template('SearchResult.html', userID=userID, recipeTitles=recipeTitles) #SearchResult.htmlを読み込む


"""
    FunctionName    :   recipeDisplay
    Data            :   2020/07/21
    Designer        :   野田啓介
    Function        :   各レシピ表示画面表示
    Entry           :   userID          --- ユーザー名
    Return          :   各レシピ画面への遷移
                        userID          --- ユーザーID
                        recipeTitle     --- レシピタイトル(str型)
                        orderthing      --- 材料名
                        recipeTime      --- 調理時間
                        recipeToCook    --- 作り方
"""
@cookme.route('/RecipeDisplay/<userID>', methods=['POST'])
def recipeDisplay(userID):

    #お気に入りのレシピを削除する
    try:
        recipeTitle = request.form['submitButton'] #お気に入りのレシピタイトル
        return redirect(url_for('cookme.favoriteDeletion', userID=userID, recipeTitle=recipeTitle)) #FavoriteDeletionメソッドに飛ぶ

    #レシピの内容を取得する
    except BadRequestKeyError:
        recipeTitle = request.form['recipeTitle']                                #レシピタイトル

        print(recipeTitle + userID)
        orderThing, recipeTime, recipeToCook = RecipeDisplay(recipeTitle)        #材料と調理時間と作り方
        historyRegister(userID, selectURL(recipeTitle), recipeTitle)             #履歴に格納
        return render_template('RecipeDisplay.html', userID=userID, 
            recipeTitle=recipeTitle, orderThing=orderThing, recipeTime=recipeTime, 
            recipeToCook=recipeToCook) #RecipeDisplay.htmlを読み込む


"""
    FunctionName    :   favorite
    Data            :   2020/07/21
    Designer        :   野田啓介
    Function        :   お気に入り表示画面の表示
    Entry           :   userID       --- ユーザー名
    Return          :   お気に入り画面に遷移
                        userID       --- ユーザーID
                        recipeTitles --- お気に入りのレシピタイトル(list型)
"""
@cookme.route('/Favorite/<userID>', methods=['POST'])
def favorite(userID):
    recipeTitles = favoriteDisplay(userID) #お気に入りのレシピ一覧
    return render_template('Favorite.html', userID=userID, recipeTitles=recipeTitles) #Favorite.htmlを読み込む


"""
    FunctionName    :   favoriteRegistration
    Data            :   2020/07/21
    Designer        :   野田啓介
    Function        :   お気に入り登録処理画面の表示
    Entry           :   userID  --- ユーザー名
    Return          :   お気に入り処理後のメッセージ出力画面に遷移
"""
@cookme.route('/FavoriteRegistration/<userID>', methods=['POST'])
def favoriteRegistration(userID):
    recipeTitle = request.form['recipeTitle']                                            #お気に入り登録するレシピタイトル
    cur.execute('SELECT recipeURL FROM cookpages WHERE recipeTitle = %s', (recipeTitle)) #お気に入りレシピのURLを取得

    registerFlag = favoriteRegister(userID, cur.fetchone()[0], recipeTitle)              #フラグ(0:登録, 1:既に登録されている)

    #お気に入りに登録するとき
    if registerFlag == 1:
        flash('お気に入りに登録しました', 'message')

    #既に登録されているとき
    else:
        flash('既にお気に入りに登録されています', 'message')
    
    return render_template('FavoriteRegistration.html') #FavoriteRegistration.htmlを読み込む


"""
    FunctionName    :   favoriteDelete
    Data            :   2020/07/04
    Designer        :   野田啓介
    Function        :   お気に入り削除処理
    Entry           :   userID --- ユーザー名
    Return          :   FavoriteDelete.htmlを読み込む
                        userID --- ユーザーID
                        recipeTitles --- 検索候補のレシピタイトル(list型)
"""
@cookme.route('/FavoriteDeletion/<userID>/<recipeTitle>', methods=['GET', 'POST'])
def favoriteDeletion(userID, recipeTitle):
    favoriteDelete(userID, recipeTitle) #お気に入りレシピの削除
    flash('削除しました', 'message')
    return render_template('FavoriteDeletion.html', userID=userID, recipeTitle=recipeTitle) #FavoriteDeletion.htmlを読み込む


"""
    FunctionName    :   history
    Data            :   2020/07/04
    Designer        :   野田啓介
    Function        :   履歴処理
    Entry           :   userID --- ユーザー名
    Return          :   SearchResult.htmlを読み込む
                        userID        --- ユーザーID
                        HistoryTitles --- 検索候補のレシピタイトル(list型)
"""
@cookme.route('/History/<userID>', methods=('GET', 'POST'))
def history(userID):
    historyTitles = historyDisplay(userID) #履歴のレシピ一覧
    return render_template('History.html', userID=userID, historyTitles=historyTitles) #History.htmlを読み込む
