"""
    C1:UI処理部
    Date:2020/6/27
    purpose:ログイン画面, 新規登録画面, ホーム画面, 検索結果画面, お気に入り画面, 
            履歴画面, レシピ表示画面を表示する
"""

from flask import Flask, render_template, request, flash, url_for
import pymysql
import C3, C4
from FavoriteMain import FavoriteRegister, FavoriteDisplay

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
    Date:           2020/6/26
    Designer:       野田 啓介
    Function:       ログイン画面を表示
    return:         Login.html --- ログイン画面のhtmlファイル

"""
@app.route('/')
def Login():
    return render_template('Login.html')



"""
    FunctionName:   Home
    Date:           2020/6/26
    Designer:       野田 啓介
    Function:       ホーム画面を表示
    return:         Home.html --- ホーム画面のhtmlファイル

"""
@app.route('/Home', methods=['POST'])
def Home():
    username = request.form['username'] #request.form['タグのクラス名']:タグのクラス名の内容を取得
    return render_template('Home.html', username=username)



"""
    FunctionName:   SignUp
    Date:           2020/6/26
    Designer:       野田 啓介
    Function:       新規登録画面
    return:         SignUp.html --- 新規登録画面のhtmlファイル

"""
@app.route('/SignUp', methods=['POST'])
def SignUp():
    return render_template('SignUp.html')



"""
    FunctionName:   Favorite
    Date:           2020/6/26
    Designer:       野田 啓介
    Function:       お気に入り画面
    return:         Favorite.html --- お気に入り画面のhtmlファイル

"""
@app.route('/Favorite/<username>', methods=['POST'])
def Favorite(username):
    recipeTitles = FavoriteDisplay(username)
    return render_template('Favorite.html', username=username, recipeTitles=recipeTitles)



"""
    FunctionName:   SearchResult
    Date:           2020/6/26
    Designer:       野田 啓介
    Function:       検索結果画面
    return:         SearchResult.html --- 検索結果画面のhtmlファイル
                    recipeTitles      --- レシピの候補一覧

"""
@app.route('/SearchResult/<username>', methods=['POST'])
def SearchResult(username):
    username = request.form['username']
    OrderThing = request.form['name1'] #材料名を取得
    recipeTitles = C3.IngredientsInputs(OrderThing)
    return render_template('SearchResult.html', username=username, recipeTitles=recipeTitles)



"""
    FunctionName:   recipeDisplay
    Date:           2020/6/26
    Designer:       野田 啓介
    Function:       レシピ表示画面
    return:         RecipeDisplay.html --- レシピ表示画面のhtmlファイル
                    recipeTitle        --- レシピのタイトル
                    OrderThing         --- 材料
                    recipeToCook       --- 作り方

"""
@app.route('/RecipeDisplay/<username>', methods=['POST'])
def RecipeDisplay(username):
    recipeTitle = request.form['recipeTitle']
    print(recipeTitle)
    OrderThing, recipeToCook = C4.recipeDisplay(recipeTitle)
    return render_template('RecipeDisplay.html', recipeTitle=recipeTitle, 
        OrderThing=OrderThing, recipeToCook=recipeToCook, username=username)



@app.route('/RecipeDisplay2/<username>', methods=['POST'])
def RecipeDisplay2(username):
    recipeTitle = request.form['recipeTitle']
    cur.execute('SELECT recipeURL FROM cookpages WHERE recipeTitle = %s', (recipeTitle))
    registerFlag = FavoriteRegister(username, cur.fetchone()[0], recipeTitle)
    if registerFlag == 1:
        flash('お気に入りに登録しました', 'message')
    else:
        flash('既にお気に入りに登録されています', 'message')

    return render_template('RecipeDisplay2.html')



"""
    FunctionName:   History
    Date:           2020/6/26
    Designer:       野田 啓介
    Function:       レシピのURLを返す
    return:         History.html --- 履歴画面のhtmlファイル 

"""
@app.route('/History', methods=['POST'])
def History():
    recipes = []
    recipeTitle = request.form['recipeTitle']
    recipes.append(recipeTitle)
    return render_template('History.html', recipes=recipes)

if __name__ == '__main__':
    app.run(debug=True)