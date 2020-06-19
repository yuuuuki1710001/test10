#レシピ一覧からレシピを検索し、材料名と作り方と調理時間を取得する
#C4:レシピ表示部

from urllib.request import urlopen
from urllib.error import URLError
from bs4 import BeautifulSoup
import C3
import pymysql

#MySQLに接続する(おまじない)
conn = pymysql.connect(
                    user='admin',
                    passwd='10pan',
                    db='cook', 
                    port=3306,
                    charset='utf8')
cur = conn.cursor()
cur.execute('USE cook')

#材料を取得する
def searchTitle(recipeTitle):

    #cookpagesから検索するレシピのURLを取得する
    cur.execute('SELECT recipeURL FROM cookpages WHERE recipeTitle = %s', (recipeTitle))
    recipeURL = cur.fetchone()[0]

    #検索するレシピのURLをオープンして、BeautifulSoupオブジェクトを作成(おまじないと思っていい)
    html = urlopen('https://cookpad.com{}'.format(recipeURL))
    soup = BeautifulSoup(html, 'html.parser')

    #タグから材料を取得する
    Stuff = soup.findAll('div', {'class':'ingredient_row'})
    recipeStuff = ''
    for stuff in Stuff:
        for foodstu, quan in zip(stuff.findAll('div', {'class':'ingredient_name'}), 
            stuff.findAll('div', {'class':'ingredient_quantity amount'})):
            foodstuffText = foodstu.get_text().replace('\n', '')
            #print(foodstuffText + ' ' + quan.get_text())
            recipeStuff += foodstuffText + ' ' + quan.get_text() + '\n'
    
    #材料を取得
    return recipeStuff
