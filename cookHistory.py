import cooksearch3
import pymysql

conn = pymysql.connect(host='172.30.24.219', 
                    port=3306,
                    user='admin',
                    passwd='10pan',
                    db='cook',
                    charset='utf8')
cur = conn.cursor()
cur.execute('USE cook')

def History_inquiry(title):
    username = 'al18087'
    cur.execute('SELECT url FROM cookpages WHERE title = %s', (title))
    url = cur.fetchone()[0]
    cur.execute('INSERT INTO history (username, url, title) VALUES (%s, %s, %s)', 
        (username, url, title))
    conn.commit()
    
