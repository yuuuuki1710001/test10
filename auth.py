import functools
from flask import Flask, Blueprint, flash, g, redirect, render_template, request, session, url_for
from db import get_db

# bp = Blueprint('auth', __name__, url_prefix='/auth')
app = Flask(__name__)

# @bp.route('/login', methods=('GET', 'POST'))
@app.route('/', methods=('GET', 'POST'))
def login():
    # GET ：ログイン画面に遷移
    # POST：ログイン処理を実施
    MODE = 1

    if request.method == 'GET':
        # ログイン画面に遷移
        return render_template('template/login.html')

    # ログインフォームから送られてきた、ユーザー名とパスワードを取得
    username = request.form['username']
    password = request.form['password']

    # DBと接続
    db = get_db(MODE, username, password)

    # ユーザー名とパスワードのチェック
    error_message = None

    if db == 1 is None:
        error_message = 'ユーザー名もしくはパスワードが正しくありません'

    if error_message is not None:
        # エラーがあればそれを表示したうえでログイン画面に遷移
        flash(error_message, category = 'alert alert-danger')
        return redirect(url_for('auth.login'))

    # エラーがなければ、セッションにユーザーIDを追加してインデックスページへ遷移
    session.clear()
    session['user_id'] = user['id']
    flash('{}さんとしてログインしました'.format(username), category = 'alert alert-info')
    return redirect(url_for('home'))


# @bp.route('/create_user', methods=('GET', 'POST'))
@app.route('/create_user', methods = ('GET', 'POST'))
def create_user():
    # GET ：ユーザー登録画面に遷移
    # POST：ユーザー登録処理を実施
    MODE = 0

    if request.method == 'GET':
        # ユーザー登録画面に遷移
        return render_template('template/create_user.html')

    # 登録フォームから送られてきた、ユーザー名とパスワードを取得
    username = request.form['username']
    password = request.form['password']

    # DBと接続
    db = get_db(MODE, username, password)

    # エラーチェック
    error_message = None
    if not username:
        error_message = 'ユーザー名の入力は必須です'
    elif not password:
        error_message = 'パスワードの入力は必須です'
    elif db == 1:
        error_message = 'ユーザー名 {} はすでに使用されています'.format(username)

    # エラーがあれば、それを画面に表示させる
    if error_message is not None:
        flash(error_message, category = 'alert alert-danger')
        return redirect(url_for('auth.create_user'))

    # ログイン画面へ遷移
    flash('ユーザー登録が完了しました。登録した内容でログインしてください', category = 'alert alert-info')
    return redirect(url_for('auth.login'))


# @bp.route('/logout')
@app.route('/logout')
def logout():
    # ログアウトする
    session.clear()
    flash('ログアウトしました', category = 'alert alert-info')
    return redirect(url_for('auth.login'))


# @bp.before_app_request
# def load_logged_in_user():
#     """
#     どのURLが要求されても、ビュー関数の前で実行される関数
#     ログインしているか確認し、ログインされていればユーザー情報を取得する
#     """
#     pass


# def login_required(view):
#     """
#     ユーザーがログインされているかどうかをチェックし、
#     そうでなければログインページにリダイレクト
#     """
#     @functools.wraps(view)
#     def wrapped_view(**kwargs):
#         if g.user is None:
#             flash('ログインをしてから操作してください', category='alert alert-warning')
#             return redirect(url_for('auth.login'))

#         return view(**kwargs)

#     return wrapped_view

if __name__ == "__main__":
    app.run(debug = True)
