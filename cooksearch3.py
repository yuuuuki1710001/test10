from urllib.request import urlopen
from urllib.error import URLError
from bs4 import BeautifulSoup
import cooksearch2
import pymysql

conn = pymysql.connect(host='172.30.24.219', 
                    port=3306,
                    user='admin',
                    passwd='10pan',
                    db='cook',
                    charset='utf8')
cur = conn.cursor()
cur.execute('USE cook')
def searchTitle(title):
    cur.execute('SELECT url FROM cookpages WHERE title = %s', (title))
    url = cur.fetchone()[0]
    html = urlopen('https://cookpad.com{}'.format(url))
    soup = BeautifulSoup(html, 'html.parser')
    Stuff = soup.findAll('div', {'class':'ingredient_row'})
    
    text = ''
    for stuff in Stuff:
        for foodstu, quan in zip(stuff.findAll('div', {'class':'ingredient_name'}), 
            stuff.findAll('div', {'class':'ingredient_quantity amount'})):
            foodstuffText = foodstu.get_text().replace('\n', '')
            print(foodstuffText + ' ' + quan.get_text())
            text += foodstuffText + ' ' + quan.get_text() + '\n'
    
    return text
