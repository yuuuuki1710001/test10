import mysql.connector as mydb

# 新規登録
def userInput(username, password):
    conn = mydb.connect(
        host     = '',
        post     = '',
        user     = '',
        password = '',
        database = ''
    )
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


# ログイン
def userOutput(username, password):
    conn = mydb.connect(
        host     = '',
        post     = '',
        user     = '',
        password = '',
        databese = ''
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
