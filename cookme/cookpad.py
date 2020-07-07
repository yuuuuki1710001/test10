from urllib.request import urlopen
from bs4 import BeautifulSoup
import pymysql
import re

conn = pymysql.connect(
                    user='admin',
                    passwd='10pan',
                    db='cook', 
                    port=3306,
                    charset='utf8')
cur = conn.cursor()
cur.execute('USE cook')


def insertUrlTitle(recipeURL, recipeTitle, OrderThing, OrderThing2, OrderThing3):

    #データベースに格納している内容を取得する
    cur.execute('SELECT * FROM cookpages WHERE recipeURL = %s'
        'AND recipeTitle = %s' 
        'AND OrderThing = %s'
        'AND OrderThing2 = %s'
        'AND OrderThing3 = %s', 
        (recipeURL, recipeTitle, OrderThing, OrderThing2, OrderThing3))

    #取得した数が0の場合はurlとタイトル名をデータベースに格納する
    if cur.rowcount == 0:
        recipeTime = -1
        cur.execute('INSERT INTO cookpages (recipeURL, recipeTitle, recipeTime, OrderThing, OrderThing2, OrderThing3)' 
        'VALUES (%s, %s, %s, %s, %s, %s)', (recipeURL, recipeTitle, recipeTime, OrderThing, OrderThing2, OrderThing3))

        #格納した情報を保存する
        conn.commit()

def loadPages():
    cur.execute('SELECT * FROM cookpages')
    pages = [row[0] for row in cur.fetchall()]
    return pages

#クローリングのやり方は深さ優先探索である
def getLinks(PageUrl, level, pages, pageURLs):
    #深さを9までにする(深さの制限はプログラマーの任意)
    if level > 9:
        return
    
    #cookpadのレシピ検索候補ページのurlをオープンする
    html = urlopen('https://cookpad.com/search{}'.format(PageUrl))
    soup = BeautifulSoup(html, 'html.parser')

    #urlオープンしたhtmlファイルからレシピのリンクを全て探す
    #それらをリストに格納する
    recipeURLs = soup.findAll('a', href=re.compile('/recipe/([0-9])*$'))
    recipeURLs = [recipeURL.attrs['href'] for recipeURL in recipeURLs]

    #リストに格納したレシピをfor文で1つ1つ調べる
    for recipeURL in recipeURLs:
        if recipeURL in pages:
            continue
        
        pages.append(recipeURL)

        #レシピのurlをオープンする
        linkhtml = urlopen('https://cookpad.com{}'.format(recipeURL))
        bs = BeautifulSoup(linkhtml, 'html.parser')

        #レシピのタイトル名を取得する
        recipeTitle = bs.find('h1').get_text()
        recipeTitle = re.sub(r'\n|\u0020|\u3000', '', recipeTitle)
        print(recipeTitle)

        #レシピの材料を取得する
        OrderThings = []
        for OrderThing in bs.findAll('div', {'class':'ingredient_name'}):
            OrderThing = OrderThing.get_text()
            OrderThings.append(OrderThing)
        
        while len(OrderThings) < 3:
            OrderThings.append('None')

        #レシピのurlとタイトルをデータベースに格納する
        insertUrlTitle(recipeURL, recipeTitle, OrderThings[0], OrderThings[1], OrderThings[2])

        #レシピのサイトの関連ワードのurlを全て見つける
        OrderThingURLs = bs.findAll('a', href=re.compile('^(/search/)((?!:).)*$'))
        OrderThingURLs = [OrderThingURL.attrs['href'] for OrderThingURL in OrderThingURLs]


        for OrderThingURL in OrderThingURLs:
            OrderThingURL = OrderThingURL.replace('/search', '')
            if OrderThingURL in pageURLs:
                continue
            pageURLs.append(OrderThingURL)

            #上記の内容を繰り返す
            getLinks(OrderThingURL, level+1, pages, pageURLs)
        
        

#検索候補ページ(材料)を生湯葉からクローリングする(材料はなんでもいい)
getLinks('/%E7%94%9F%E6%B9%AF%E8%91%89', 0, loadPages(), [])
cur.close()
conn.close()