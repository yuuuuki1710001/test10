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

def HistoryRegister(UserID,recipeURL,recipeTitle):
    cur.execute('INSERT INTO history (UserID,recipeURL,recipeTitle) VALUES (%s,%s,%s)',(UserID, recipeURL, recipeTitle))
    conn.commit()

def HistoryDisplay(userID):
    historyTitles = []
    cur.execute('SELECT * FROM history WHERE UserID = %s',(userID))
    historyTitles = [row[2] for row in cur.fetchall()]
    return historyTitles