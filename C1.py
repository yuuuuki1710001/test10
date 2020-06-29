"""
    C1:UI処理部
    Date:2020/6/30
    purpose:ログイン画面, 新規登録画面, ホーム画面, 検索結果画面, お気に入り登録画面
    お気に入り表示画面, お気に入り削除画面, 履歴画面, レシピ表示画面を表示する
"""

from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.exceptions import BadRequestKeyError
import pymysql
import C3
from C4 import selectURL, recipeDisplay
from FavoriteMain import FavoriteRegister, FavoriteDisplay
from HistoryMain import HistoryRegister, HistoryDisplay

#MySQLに接続する(おまじない)
conn = pymysql.connect(
                    user='admin',
                    passwd='10pan',
                    db='cook', 
                    port=3306,
                    charset='utf8')
cur = conn.cursor()
cur.execute('USE cook')

app = Flask(__name__)
app.config["SECRET_KEY"] = "sample1203"


"""
    FunctionName:   Login
    Date:           2020/6/30
    Designer:       野田 啓介
    Function:       ログイン画面を表示
    return:         Login.html --- ログイン画面のhtmlファイル

"""
@app.route('/')
def Login():
    return render_template('Login.html')



"""
    FunctionName:   Home
    Date:           2020/6/30
    Designer:       野田 啓介
    Function:       ホーム画面を表示
    return:         Home.html --- ホーム画面のhtmlファイル
                    userID    --- ユーザID(str型)

"""
@app.route('/Home', methods=['POST'])
def Home():
    userID = request.form['userID'] #ユーザーIDを取得
    return render_template('Home.html', userID=userID)



"""
    FunctionName:   SignUp
    Date:           2020/6/30
    Designer:       野田 啓介
    Function:       新規登録画面
    return:         SignUp.html --- 新規登録画面のhtmlファイル

"""
@app.route('/SignUp', methods=['POST'])
def SignUp():
    return render_template('SignUp.html')



"""
    FunctionName:   Favorite
    Date:           2020/6/30
    Designer:       野田 啓介
    Function:       お気に入り画面
    entry:          userID        --- ユーザーID(str型)
    return:         Favorite.html --- お気に入り画面のhtmlファイル
                    userID        --- ユーザーID(str型)
                    recipeTitles  --- お気に入り登録しているレシピ一覧(list型)

"""
@app.route('/Favorite/<userID>', methods=['POST'])
def Favorite(userID):
    recipeTitles = FavoriteDisplay(userID) #お気に入り登録しているレシピ一覧を取得
    return render_template('Favorite.html', userID=userID, recipeTitles=recipeTitles)



"""
    FunctionName:   FavoriteDelete
    Date:           2020/6/30
    Designer:       野田 啓介
    Function:       お気に入り削除画面
    entry:          userID              --- ユーザーID(str型)
    return:         FavoriteDelete.html --- お気に入り画面のhtmlファイル
                    userID              --- ユーザーID(str型)

"""
@app.route('/FavoriteDelete/<userID>', methods=['GET', 'POST'])
def FavoriteDelete(userID):
    flash('削除しました', 'message') #削除のメッセージ
    return render_template('FavoriteDelete.html', userID=userID)



"""
    FunctionName:   SearchResult
    Date:           2020/6/30
    Designer:       野田 啓介
    Function:       検索結果画面
    entry:          userID            --- ユーザーID(str型)
    return:         SearchResult.html --- 検索結果画面のhtmlファイル
                    userID            --- ユーザーID(str型)
                    recipeTitles      --- レシピの候補一覧(list型)

"""
@app.route('/SearchResult/<userID>', methods=['POST'])
def SearchResult(userID):
    userID = request.form['userID']                 #ユーザーIDを取得
    OrderThing = request.form['name1']              #材料名を取得
    recipeTitles = C3.IngredientsInputs(OrderThing) #レシピの検索候補一覧を取得
    return render_template('SearchResult.html', userID=userID, recipeTitles=recipeTitles)



"""
    FunctionName:   recipeDisplay
    Date:           2020/6/30
    Designer:       野田 啓介
    Function:       レシピ表示画面
    entry:          userID             --- ユーザーID(str型)
    return:         RecipeDisplay.html --- レシピ表示画面のhtmlファイル
                    recipeTitle        --- レシピのタイトル(str型)
                    OrderThing         --- 材料(str型)
                    recipeToCook       --- 作り方(str型)
                    userID             --- ユーザーID(str型)

"""
@app.route('/RecipeDisplay/<userID>', methods=['POST'])
def RecipeDisplay(userID):

    #お気に入りレシピを削除するときの処理
    try: 
        recipeTitle = request.form['submit_button'] #お気に入り登録から削除したいレシピ
        return redirect(url_for('FavoriteDelete', userID=userID))

    #レシピの検索候補からレシピを調べるときの処理
    except BadRequestKeyError:
        recipeTitle = request.form['recipeTitle']                    #調べたいレシピ
        print(recipeTitle)
        OrderThing, recipeToCook = recipeDisplay(recipeTitle)        #レシピの材料と作り方
        HistoryRegister(userID, selectURL(recipeTitle), recipeTitle) #履歴に登録
        return render_template('RecipeDisplay.html', recipeTitle=recipeTitle, 
            OrderThing=OrderThing, recipeToCook=recipeToCook, userID=userID)
        


"""
    FunctionName:   FavoriteRegistration
    Date:           2020/6/30
    Designer:       野田 啓介
    Function:       レシピ表示画面
    entry:          userID                    --- ユーザーID(str型)
    return:         FavoriteRegistration.html --- レシピ表示画面のhtmlファイル
"""
@app.route('/FavoriteRegistration/<userID>', methods=['POST'])
def FavoriteRegistration(userID):
    recipeTitle = request.form['recipeTitle'] #お気に入り登録するレシピ
    cur.execute('SELECT recipeURL FROM cookpages WHERE recipeTitle = %s', (recipeTitle))

    registerFlag = FavoriteRegister(userID, cur.fetchone()[0], recipeTitle) #

    #お気に入り登録されていないとき
    if registerFlag == 0: 
        flash('お気に入りに登録しました', 'message')

    #既にお気に入り登録されているとき
    else:                 
        flash('既にお気に入りに登録されています', 'message')

    return render_template('FavoriteRegistration.html')



"""
    FunctionName:   History
    Date:           2020/6/30
    Designer:       野田 啓介
    Function:       レシピのURLを返す
    entry:          userID        --- ユーザーID(str型)
    return:         History.html  --- 履歴画面のhtmlファイル 
                    userID        --- ユーザーID(str型)
                    historyTitles --- 履歴のレシピ一覧(list型)

"""
@app.route('/History/<userID>', methods=['POST'])
def History(userID):
    historyTitles = HistoryDisplay(userID) #履歴のレシピ一覧を取得
    return render_template('History.html', userID=userID, historyTitles=historyTitles)

if __name__ == '__main__':
    app.run(debug=True)