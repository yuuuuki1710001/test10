from flask import Flask, render_template, request
import cooksearch2, cooksearch3, cookHistory

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('login.html')


@app.route('/main_frame', methods=['POST'])
def main_frame():
    name = request.form['name'] #request.form['タグのクラス名']:タグのクラス名の内容を取得
    return render_template('main_frame.html', name=name)

@app.route('/favorite', methods=['POST'])
def favorite():
    return render_template('favorite.html')

@app.route('/frame1', methods=['POST'])
def frame1():
    stufffood = request.form['name1'] #材料名を取得
    searchTitles = cooksearch2.selectTitle(stufffood)
    return render_template('frame1.html', searchTitles=searchTitles)

@app.route('/frame2', methods=['POST'])
def frame2():
    recipeTitle = request.form['recipe']
    print(recipeTitle)
    recipe = cooksearch3.searchTitle(recipeTitle)
    return render_template('frame2.html', recipeTitle=recipeTitle, recipe=recipe)

@app.route('/history', methods=['POST'])
def history():
    recipes = []
    recipeTitle = request.form['recipeTitle']
    recipes.append(recipeTitle)
    cookHistory.History_inquiry(recipeTitle)
    return render_template('history.html', recipes=recipes)

if __name__ == '__main__':
    app.run(debug=True)