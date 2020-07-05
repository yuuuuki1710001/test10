"""
    C7      :   利用者情報管理部
    Data    :   2020/06/28
    Purpose :   利用者情報のデータベース処理
"""

# import mysql.connector as mydb
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash

"""
    FunctionName    :   userInput
    Data            :   2020/06/30
    Designer        :   前原達也
    Function        :   新規登録のためのデータベース操作
    Return          :   0...入力内容とデータベース内の情報が一致, 1...入力内容とデータベース内の情報が不一致
"""
def userInput(username, password):
    # パスワードをハッシュ化
    Pass = generate_password_hash(password)
    
    conn = pymysql.connect(
        host        = '172.30.27.88',
        port        = 3306,
        user        = 'admin',
        passwd    = '10pan',
        db          = 'cook'
    )
    conn.ping(reconnect = True)

    cur = conn.cursor()
    cur.execute('USE cook')

    cur.execute('CREATE TABLE IF NOT EXISTS user(UserID VARCHAR(256), Pass VARCHAR(512), PRIMARY KEY(UserID))')
    cur.execute('SELECT UserID FROM user WHERE UserID = %s', (username))

    if cur.rowcount == 1:
        cur.close()
        conn.close()
        return 1
    elif (cur.rowcount == 0):
        cur.execute('INSERT INTO user(UserID, Pass) VALUES(%s, %s);', (username, Pass))
        conn.commit()
        cur.close()
        conn.close()
        return 0


"""
    FunctionName    :   userOutput
    Data            :   2020/06/28
    Designer        :   前原達也
    Function        :   ログインのためのデータベース操作
    Return          :   0...入力内容とデータベース内の情報が一致, 1...入力内容とデータベース内の情報が不一致
"""
def userOutput(username, password):
    conn = pymysql.connect(
        host        = '172.30.27.88',
        port        = 3306,
        user        = 'admin',
        passwd    = '10pan',
        db          = 'cook'
    )
    conn.ping(reconnect = True)

    cur = conn.cursor()
    cur.execute('USE cook')

    cur.execute('SELECT Pass FROM user WHERE UserID = %s;', (username))

    if cur.rowcount == 0:
        cur.close()
        conn.close()
        return 1
    else:
        data = cur.fetchone()
        
        if check_password_hash(data[0], password):
            cur.close()
            conn.close()
            return 0
        
        return 1
