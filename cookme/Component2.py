"""
    C2      :   認証処理部
    Date    :   2020/07/16
    Purpose :   ログイン処理、新規登録処理、ログアウト処理
"""

import functools
import os
from flask import Flask, Blueprint, flash, g, redirect, render_template, request, session, url_for
from cookme.Component1 import home
from cookme.Component7 import userInput, userOutput

user = Blueprint('user', __name__)

"""
    FunctionName    :   login
    Data            :   2020/07/21
    Designer        :   前原達也
    Function        :   利用者のログイン処理
    Entry           :   userID      --- ユーザーID
                        passWord    --- パスワード
                        ※ 上記の入力はhtmlの入力フォームからの入力
    Return          :   セッションを保存し、利用者のホーム画面に遷移
"""
@user.route('/', methods=('GET', 'POST'))
def login():
    # GET ：ログイン画面に遷移
    # POST：ログイン処理を実施

    if request.method == 'GET':
        # ログイン画面に遷移
        return render_template('login.html')

    # ログインフォームから送られてきた、ユーザー名とパスワードを取得
    userID = request.form['userID']
    passWord = request.form['password']

    # DBと接続
    db = userOutput(userID, passWord)

    # ユーザー名とパスワードのチェック
    error_message = None
    if not userID:
        error_message = 'ユーザー名の入力は必須です'
    elif not passWord:
        error_message = 'パスワードの入力は必須です'
    elif db == 1:
        error_message = 'ユーザー名もしくはパスワードが正しくありません'

    if error_message is not None:
        # エラーがあればそれを表示したうえでログイン画面に遷移
        flash(error_message, 'message')
        return redirect(url_for('user.login'))

    # エラーがなければ、セッションにユーザーIDを追加してインデックスページへ遷移
    session.clear()
    session['username'] = userID
    flash('{}さんとしてログインしました'.format(userID), 'message')
    return redirect(url_for('cookme.home', userID=userID))


"""
    FunctionName    :   createUser
    Data            :   2020/07/21
    Designer        :   前原達也
    Function        :   利用者の新規登録処理
    Entry           :   userID      --- ユーザーID
                        passWord    --- パスワード
                        ※ 上記の入力はhtmlの入力フォームからの入力
    Return          :   データベースに利用者情報を格納し、ログイン画面に遷移
"""
@user.route('/create_user', methods=('GET', 'POST'))
def createUser():
    # GET ：ユーザー登録画面に遷移
    # POST：ユーザー登録処理を実施

    if request.method == 'GET':
        # ユーザー登録画面に遷移
        return render_template('CreateUser.html')

    # 登録フォームから送られてきた、ユーザー名とパスワードを取得
    userID = request.form['userID']
    passWord = request.form['password']

    # DBと接続
    db = userInput(userID, passWord)

    # エラーチェック
    error_message = None
    if not userID:
        error_message = 'ユーザー名の入力は必須です'
    elif not passWord:
        error_message = 'パスワードの入力は必須です'
    elif db == 1:
        error_message = 'ユーザー名 {} はすでに使用されています'.format(userID)
    elif db == 2:
        error_message = 'ユーザー名は英数字とアンダーバーのみ使用できます'
    elif db == 3:
        error_message = 'パスワードには英数字を1字以上含めてください'
    elif db == 4:
        error_message = 'パスワードが短いです'
    elif db == 5:
        error_message = 'パスワードが長いです'

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
def logout():
    # ログアウトする
    session.clear()
    flash('ログアウトしました', category = 'alert alert-info')
    return redirect(url_for('user.login'))
