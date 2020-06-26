"""
    C1:UI処理部
    Date:2020/6/26
    purpose:ログイン画面, 新規登録画面, ホーム画面, 検索結果画面, お気に入り画面, 
            履歴画面, レシピ表示画面を表示する
"""

from flask import Flask, render_template, request
import C3, C4

app = Flask(__name__)


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
    name = request.form['name'] #request.form['タグのクラス名']:タグのクラス名の内容を取得
    return render_template('Home.html', name=name)



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
@app.route('/Favorite', methods=['POST'])
def Favorite():
    return render_template('Favorite.html')



"""
    FunctionName:   SearchResult
    Date:           2020/6/26
    Designer:       野田 啓介
    Function:       検索結果画面
    return:         SearchResult.html --- 検索結果画面のhtmlファイル
                    recipeTitles      --- レシピの候補一覧

"""
@app.route('/SearchResult', methods=['POST'])
def SearchResult():
    OrderThing = request.form['name1'] #材料名を取得
    recipeTitles = C3.IngredientsInputs(OrderThing)
    return render_template('SearchResult.html', recipeTitles=recipeTitles)



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
@app.route('/RecipeDisplay', methods=['POST'])
def RecipeDisplay():
    recipeTitle = request.form['recipe']
    print(recipeTitle)
    OrderThing, recipeToCook = C4.recipeDisplay(recipeTitle)
    return render_template('RecipeDisplay.html', recipeTitle=recipeTitle, 
        OrderThing=OrderThing, recipeToCook=recipeToCook)



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