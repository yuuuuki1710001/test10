import pymysql

conn = pymysql.connect(
                    user='admin',
                    passwd='10pan',
                    db='cook',
                    port = 3306,
                    charset = 'utf8'
)

cur = conn.cursor()
cur.execute('USE cook')

"""
FunctionName : FavoriteRegister
Date : 6/30
Designer : 橋本優希
Function : お気に入り登録
Entry : C1.py
Return : C1.py
"""
def FavoriteRegister(UserID,recipeURL,recipeTitle):
    cur.execute('SELECT * FROM favorite WHERE UserID = %s'
               'AND recipeURL = %s'
               'AND recipeTitle = %s',(UserID, recipeURL, recipeTitle))

    if cur.rowcount == 0 :
        cur.execute('INSERT INTO favorite (UserID,recipeURL,recipeTitle) VALUES (%s,%s,%s)',(UserID, recipeURL, recipeTitle))
        conn.commit()
        return 1

    return 0

"""
FunctionName : FavoriteDisplay
Date : 6/30
Designer : 橋本優希
Function : お気に入り登録したレシピの表示
Entry : C1.py
Return : C1.py
"""
def FavoriteDisplay(UserID):
    favoriteTitles = []
    cur.execute('SELECT * FROM favorite WHERE UserID = %s', (UserID))
    favoriteTitles = [row[2] for row in cur.fetchall()]
    return favoriteTitles

"""
FunctionName : FavoriteDelete
Date : 6/30
Designer : 橋本優希
Function : お気に入り登録したレシピの削除
Entry : C1.py
Return : なし
"""
def FavoriteDelete(UserID,recipeTitle):
    cur.execute('DELETE FROM favorite WHERE UserID = %s'
               'AND recipeTitle = %s',(UserID, recipeTitle))
    conn.commit()