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
FunctionName : HistoryRegister
Date : 6/30
Designer : 橋本優希
Function : 履歴登録
Entry : C1.py
Return : なし
"""
def HistoryRegister(UserID,recipeURL,recipeTitle):
    cur.execute('INSERT INTO history (UserID,recipeURL,recipeTitle) VALUES (%s,%s,%s)',(UserID, recipeURL, recipeTitle))
    conn.commit()

"""
FunctionName : HistoryDisplay
Date : 6/30
Designer : 橋本優希
Function : 履歴表示
Entry : C1.py
Return : C1.py
"""
def HistoryDisplay(UserID):
    historyTitles = []
    cur.execute('SELECT * FROM history WHERE UserID = %s',(UserID))
    historyTitles = [row[2] for row in cur.fetchall()]
    return historyTitles