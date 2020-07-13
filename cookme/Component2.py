"""
    C2      :   認証処理部
    Data    :   2020/07/06
    Purpose :   ログイン処理、新規登録処理、ログアウト処理
"""

import functools
import os
from flask import Flask, Blueprint, flash, g, redirect, render_template, request, session, url_for
from cookme.Component1 import Home
from cookme.Component7 import userInput, userOutput

user = Blueprint('user', __name__)

"""
    FunctionName    :   login
    Data            :   2020/07/06
    Designer        :   前原達也
    Function        :   利用者のログイン処理
    Entry           :   利用者ID、パスワード
    Return          :   セッションを保存し、利用者のホーム画面に遷移
"""
@user.route('/', methods=('GET', 'POST'))
#@app.route('/', methods=('GET', 'POST'))
def login():
    # GET ：ログイン画面に遷移
    # POST：ログイン処理を実施

    if request.method == 'GET':
        # ログイン画面に遷移
        return render_template('login.html')

    # ログインフォームから送られてきた、ユーザー名とパスワードを取得
    UserID = request.form['UserID']
    Pass = request.form['password']

    # DBと接続
    db = userOutput(UserID, Pass)

    # ユーザー名とパスワードのチェック
    error_message = None
    if not UserID:
        error_message = 'ユーザー名の入力は必須です'
    elif not Pass:
        error_message = 'パスワードの入力は必須です'
    elif db == 1:
        error_message = 'ユーザー名もしくはパスワードが正しくありません'
        print(error_message)

    if error_message is not None:
        # エラーがあればそれを表示したうえでログイン画面に遷移
        flash(error_message, 'message')
        return redirect(url_for('user.login'))

    # エラーがなければ、セッションにユーザーIDを追加してインデックスページへ遷移
    session.clear()
    session['username'] = UserID
    flash('{}さんとしてログインしました'.format(UserID), 'message')
    return redirect(url_for('cookme.Home', userID=UserID))


"""
    FunctionName    :   createUser
    Data            :   2020/07/04
    Designer        :   前原達也
    Function        :   利用者の新規登録処理
    Entry           :   利用者ID、パスワード
    Return          :   データベースに利用者情報を格納し、ログイン画面に遷移
"""
@user.route('/create_user', methods=('GET', 'POST'))
#@app.route('/create_user', methods = ('GET', 'POST'))
def createUser():
    # GET ：ユーザー登録画面に遷移
    # POST：ユーザー登録処理を実施

    if request.method == 'GET':
        # ユーザー登録画面に遷移
        return render_template('CreateUser.html')

    # 登録フォームから送られてきた、ユーザー名とパスワードを取得
    UserID = request.form['UserID']
    Pass = request.form['password']

    # DBと接続
    db = userInput(UserID, Pass)

    # エラーチェック
    error_message = None
    if not UserID:
        error_message = 'ユーザー名の入力は必須です'
    elif not Pass:
        error_message = 'パスワードの入力は必須です'
    elif db == 1:
        error_message = 'ユーザー名 {} はすでに使用されています'.format(UserID)

    # エラーがあれば、それを画面に表示させる
    if error_message is not None:
        flash(error_message, 'message')
        return redirect(url_for('user.createUser'))

    # ログイン画面へ遷移
    flash('ユーザー登録が完了しました。登録した内容でログインしてください', 'message')
    return redirect(url_for('user.login'))


"""
    FunctionName    :   logout
    Data            :   2020/07/04
    Designer        :   前原達也
    Function        :   ログアウト処理
    Entry           :   なし
    Return          :   セッションを破棄し、ログイン画面に遷移
"""
@user.route('/logout')
#@app.route('/logout')
def logout():
    # ログアウトする
    session.clear()
    flash('ログアウトしました', category = 'alert alert-info')
    return redirect(url_for('user.login'))



# @bp.before_app_request
# @app.before_request
# def load_logged_in_user():
#     # どのURLが要求されても、ビュー関数の前で実行される関数
#     # ログインしているか確認し、ログインされていればユーザー情報を取得する

#     UserID = session.get('UserID')

#     if UserID is None:
#         g.user = None
#     else:
#         db = 

# def login_required(view):
#     # ユーザーがログインされているかどうかをチェックし、
#     # そうでなければログインページにリダイレクト
#     @functools.wraps(view)
#     def wrapped_view(**kwargs):
#         if g.user is None:
#             flash('ログインをしてから操作してください', category='alert alert-warning')
#             return redirect(url_for('auth.login'))

#         return view(**kwargs)

#     return wrapped_view

#if __name__ == "__main__":
    #app.run(debug = True)
