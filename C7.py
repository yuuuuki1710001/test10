"""
    C7      :   利用者情報管理部
    Data    :   2020/06/28
    purpose :   利用者情報のデータベース処理
"""

import mysql.connector as mydb

"""
    FunctionName    :   userInput
    Data            :   2020/06/28
    Designer        :   前原達也
    Function        :   新規登録のためのデータベース操作
    return          :   0...入力内容とデータベース内の情報が一致, 1...入力内容とデータベース内の情報が不一致
"""
def userInput(username, password):
    conn = mydb.connect(
        host     = 'localhost',
        post     = '3306',
        user     = 'root',
        password = 'baskdrag1421_mysql',
        databese = 'local'
    conn.ping(reconnect = True)

    cur = conn.cursor()
    cur.execute('USE cook')

    cur.execute('CREATE TABLE IF NOT EXISTS user(UserID VARCHER(256), Pass VARCHER(256), PRIMARY KEY(UserID));')
    cur.execute('SELECT UserID FROM user WHERE UserID = %s', (username))

    if cur.rowcount == 1:
        cur.close()
        conn.close()
        return 1
    elif (cur.rowcount == 0):
        cur.execute('INSERT INTO user(UserID, Pass) VALUES(%s, %s);', (username, password))
        conn.commit()
        cur.close()
        conn.close()
        return 0


"""
    FunctionName    :   userOutput
    Data            :   2020/06/28
    Designer        :   前原達也
    Function        :   ログインのためのデータベース操作
    return          :   0...入力内容とデータベース内の情報が一致, 1...入力内容とデータベース内の情報が不一致
"""
def userOutput(username, password):
    conn = mydb.connect(
        host     = 'localhost',
        post     = '3306',
        user     = 'root',
        password = 'baskdrag1412_mysql',
        databese = 'local'
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
        
        if password == data[0]:
            cur.close()
            conn.close()
            return 0
        elif password != data[0]:
            cur.close()
            conn.close()
            return 1
