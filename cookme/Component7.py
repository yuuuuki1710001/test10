"""
    C7      :   利用者情報管理部
    Date    :   2020/07/16
    Purpose :   利用者情報のデータベース処理
"""

import re
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash

"""
    FunctionName    :   userInput
    Data            :   2020/07/21
    Designer        :   前原達也
    Function        :   新規登録のためのデータベース操作
    Entry           :   userID      --- 利用者ID
                        passWord    --- パスワード
    Return          :   0           --- 入力内容とデータベース内の情報が一致(正常処理)
                        1           --- 入力内容とデータベース内の情報が不一致(異常処理)
                        2           --- IDに英数字と"_"以外が含まれた時(異常処理)
                        3           --- パスワードに英数字が1文字も含まれていない時(異常処理)
                        4           --- パスワードの長さ制限外(minimum)(異常処理)
                        5           --- パスワードの長さ制限外(maximum)(異常処理)
                        
"""
def userInput(userID, passWord):
    # 利用者名は英数字と"_"のみ
    if re.search('\W', userID):
        return 2
    # パスワードに英数字が1文字も含まれていない
    if re.search('[a-zA-Z0-9]', passWord) == None:
        return 3
    # パスワードの長さ制限
    if len(passWord) < 8:
        return 4
    if len(passWord) > 16:
        return 5

    # パスワードをハッシュ化
    passWord = generate_password_hash(passWord)
    
    # MySQL接続
    conn = pymysql.connect(
        user    =   'root',
        passwd  =   '10pan',
        db      =   'cook',
        port    =   3306,
        charset =   'utf8'
    )
    conn.ping(reconnect = True)

    cur = conn.cursor()
    cur.execute('USE cook')

    cur.execute('CREATE TABLE IF NOT EXISTS user(UserID VARCHAR(256), pass VARCHAR(512), PRIMARY KEY(UserID))')
    cur.execute('SELECT UserID FROM user WHERE UserID = %s', (userID))

    if cur.rowcount == 1:
        cur.close()
        conn.close()
        return 1
    elif (cur.rowcount == 0):
        cur.execute('INSERT INTO user(userID, pass) VALUES(%s, %s);', (userID, passWord))
        conn.commit()
        cur.close()
        conn.close()
        return 0


"""
    FunctionName    :   userOutput
    Data            :   2020/07/21
    Designer        :   前原達也
    Function        :   ログインのためのデータベース操作
    Entry           :   userID      --- 利用者ID
                        passWord    --- パスワード
    Return          :   0           --- 入力内容とデータベース内の情報が一致(正常格納)
                        1           --- 入力内容とデータベース内の情報が不一致(格納不可)
"""
def userOutput(userID, passWord):
    conn = pymysql.connect(
        user    =   'root',
        passwd  =   '10pan',
        db      =   'cook',
        port    =   3306,
        charset =   'utf8'
    )
    conn.ping(reconnect = True)

    cur = conn.cursor()
    cur.execute('USE cook')

    cur.execute('SELECT pass FROM user WHERE UserID = %s;', (userID))

    if cur.rowcount == 0:
        cur.close()
        conn.close()
        return 1
    else:
        data = cur.fetchone()
        
        if check_password_hash(data[0], passWord) == 1:
            cur.close()
            conn.close()
            return 0
        
        return 1

