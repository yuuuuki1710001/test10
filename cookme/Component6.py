"""
    C6      :   履歴部
    Data    :   2020/07/21
    Purpose :   履歴のデータベース操作
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
    FunctionName    :   historyRegister
    Date            :   2020/07/21
    Designer        :   橋本優希
    Function        :   閲覧したレシピの保存(閲覧した時点でデータベースに格納する)するためのデータベース操作
    Entry           :   userID      --- 利用者ID
                        recipiURL   --- 閲覧したレシピのURL
                        recipiTitle --- 閲覧したレシピのタイトル
    Return          :   なし
"""
def historyRegister(userID,recipeURL,recipeTitle):
    cur.execute('INSERT INTO history (UserID,recipeURL,recipeTitle) VALUES (%s,%s,%s)',(userID, recipeURL, recipeTitle))
    conn.commit()
    

"""
    FunctionName    :   historyDisplay
    Date            :   2020/07/21
    Designer        :   橋本優希
    Function        :   閲覧したレシピの表示(履歴表示)させるためのデータベース操作
    Entry           :   userID          --- 利用者ID
    Return          :   histryTitles    --- 閲覧したレシピ(List型)
"""
def historyDisplay(userID):
    historyTitles = []
    cur.execute('SELECT * FROM history WHERE UserID = %s',(userID))
    historyTitles = [row[2] for row in cur.fetchall()]
    return historyTitles
    