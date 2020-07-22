"""
    C5      :   お気に入り部
    Date    :   2020/07/21
    Purpose :   お気に入りのデータベース操作
"""

import pymysql

# MySQL接続
conn = pymysql.connect(
    user    =   'root',
    passwd  =   '10pan',
    db      =   'cook',
    port    =   3306,
    charset =   'utf8'
)

cur = conn.cursor()
cur.execute('USE cook')

"""
    FunctionName :  favoriteRegister
    Date         :  2020/07/21
    Designer     :  橋本優希
    Function     :  お気に入りへの登録のためのデータベース操作
    Entry        :  userID      --- ユーザーID
                    recipiUrl   --- お気に入り登録をしたいレシピのURL
                    recipiTitle --- お気に入り登録をしたいレシピのタイトル
    Return       :  0           --- 既にデータベースに格納されているため、格納不可
                    1           --- データベースへの正常格納
"""
def favoriteRegister(userID,recipeUrl,recipeTitle):
    cur.execute('SELECT * FROM favorite WHERE UserID = %s'
               'AND recipeURL = %s'
               'AND recipeTitle = %s',(userID, recipeUrl, recipeTitle))

    if cur.rowcount == 0 :
        cur.execute('INSERT INTO favorite (UserID,recipeURL,recipeTitle) VALUES (%s,%s,%s)',(userID, recipeUrl, recipeTitle))
        conn.commit()
        return 1

    return 0


"""
    FunctionName    :   favoriteDisplay
    Date            :   2020/07/21
    Designer        :   橋本優希
    Function        :   お気に入り登録したレシピの表示するためのデータベース操作
    Entry           :   userID  --- 利用者ID
    Return          :   favoriteTitle   --- 利用者IDに対応するお気に入り登録済のレシピのタイトル
"""
def favoriteDisplay(userID):
    favoriteTitles = []
    cur.execute('SELECT * FROM favorite WHERE UserID = %s', (userID))
    favoriteTitles = [row[2] for row in cur.fetchall()]
    return favoriteTitles


"""
    FunctionName    :   favoriteDelete
    Date            :   2020/06/30
    Designer        :   橋本優希
    Function        :   お気に入り登録したレシピの削除するデータベース操作
    Entry           :   userID      --- 利用者ID
                        recipiTitle --- お気に入り登録されているレシピのタイトル
    Return          :   なし
"""
def favoriteDelete(userID,recipeTitle):
    cur.execute('DELETE FROM favorite WHERE UserID = %s AND recipeTitle = %s',(userID, recipeTitle))
    conn.commit()
    