import mysql.connector as mydb

def get_db(MODE, username, password):
    conn = mydb.connect(
        host     = 'localhost',
        post     = '3306',
        user     = 'root',
        password = 'baskdrag1412_mysql',
        databese = 'cook'
    )
    conn.ping(reconnect = True)

    cur = conn.cursor()
    # cur.execute('use cook')

    # 登録
    if MODE == 0:
        cur.execute('create table if not exists user(UserID varchar(256), Pass varcher(256), primary key(UserID));')

        cur.execute('select UserID from user where UserID = %s', (username))
        if cur.rowcount == 1: return 1
        elif (cur.rowcount == 0):
            cur.execute('insert into user(UserID, password) values(%s, %s);', (username, password))
            conn.commit()
            return 0

    # ログイン
    elif MODE == 1:
        cur.execute('select password from user where UserID = %s;', (username))

        for i in range(cur.rowcount):
            data = cur.fetchall()
            
            if password == data: return 0
            elif password != data: return 1


# def close_db(e = None):