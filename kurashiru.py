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


def insertUrlTitle(recipeURL, recipeTitle, recipeTime, OrderThing, OrderThing2, OrderThing3):

    #データベースに格納している内容を取得する
    cur.execute('SELECT * FROM cookpages WHERE recipeURL = %s'
        'AND recipeTitle = %s'
        'AND recipeTime = %s',
        (recipeURL, recipeTitle, recipeTime))

    #取得した数が0の場合はurlとタイトル名をデータベースに格納する
    if cur.rowcount == 0:
        cur.execute('INSERT INTO cookpages (recipeURL, recipeTitle, recipeTime, OrderThing, OrderThing2, OrderThing3)' 
        'VALUES (%s, %s, %s, %s, %s, %s)', (recipeURL, recipeTitle, recipeTime, OrderThing, OrderThing2, OrderThing3))

        #格納した情報を保存する
        conn.commit()

#recipeURLをリストに格納する
def loadPages():
    cur.execute('SELECT * FROM cookpages')
    pages = [row[0] for row in cur.fetchall()]
    return pages

#レシピの検索一覧とレシピを交互にたどってクローリングする
def getLinks(pageURL, level, pages, pageURLs):

    #深さを9までとする
    if level > 9:
        return
    

    #cookpadのレシピ検索候補ページのURLをオープンする
    html = urlopen('https://www.kurashiru.com{}'.format(pageURL))
    soup = BeautifulSoup(html, 'html.parser')

    #URLオープンしたhtmlファイルからレシピのリンクを全て探す
    #それらをリストに格納する
    recipeURLs = soup.findAll('a', href=re.compile('/recipes/'))
    recipeURLs = [recipeURL.attrs['href'] for recipeURL in recipeURLs]

    #リストに格納したレシピをfor文で1つ1つ調べる
    for recipeURL in recipeURLs:
        if recipeURL in pages:
            continue
        
        pages.append(recipeURL)

        #レシピのURLをオープンする
        linkhtml = urlopen('https://www.kurashiru.com{}'.format(recipeURL))
        bs = BeautifulSoup(linkhtml, 'html.parser')

        #レシピのタイトル名を取得する
        recipeTitle = bs.find('h1').get_text()
        recipeTitle = re.sub(r'\n|\u0020|\u3000|レシピ・作り方', '', recipeTitle)
        print(recipeTitle)

        #レシピの調理時間を取得する
        try:
            recipeTime = bs.find('p', {'class':'cooking-time'}).get_text()
            recipeTime = re.sub(r'調理時間：|分|\n|\u0020', '', recipeTime)
            recipeTime = int(recipeTime)
        except AttributeError:
            recipeTime = -1

        #レシピの材料を取得する
        OrderThings = []
        for OrderThing in bs.findAll('span', {'class':'ingredient-name'}):
            OrderThing = OrderThing.get_text()
            OrderThings.append(OrderThing)
        while len(OrderThings) < 3:
            OrderThings.append('None')

        #レシピのURLとタイトルと調理時間をデータベースに格納する
        insertUrlTitle(recipeURL, recipeTitle, recipeTime, 
            OrderThings[0], OrderThings[1], OrderThings[2])

        #レシピのサイトの関連ワードのURLを全て見つける
        OrderThingURLs = bs.findAll('a', href=re.compile('/video_categories/'))
        OrderThingURLs = [OrderThingURL.attrs['href'] + '?page=44' for OrderThingURL in OrderThingURLs]

        for OrderThingURL in OrderThingURLs:

            #一度クローリングした関連ワードのURLは無視する
            #まだクローリングしていない関連ワードのURLをpageURLリストに格納する
            if OrderThingURL in pageURLs:
                continue
            pageURLs.append(OrderThingURL)

            #上記の内容を繰り返す
            getLinks(OrderThingURL, level+1, pages, pageURLs)

#検索候補ページ(材料)を野菜からクローリングする(材料はなんでもいい)
getLinks('/video_categories/244?page=42', 0, loadPages(), [])
cur.close()
conn.close()