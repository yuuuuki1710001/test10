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
    cur.execute('SELECT * FROM cookpages2 WHERE recipeURL = %s'
        'AND recipeTitle = %s'
        'AND recipeTime = %s', 
        (recipeURL, recipeTitle, recipeTime))

    #取得した数が0の場合はurlとタイトル名をデータベースに格納する
    if cur.rowcount == 0:
        cur.execute('INSERT INTO cookpages2 (recipeURL, recipeTitle, recipeTime, OrderThing, OrderThing2, OrderThing3)' 
        'VALUES (%s, %s, %s, %s, %s, %s)', (recipeURL, recipeTitle, recipeTime, OrderThing, OrderThing2, OrderThing3))

        #格納した情報を保存する
        conn.commit()

#recipeURLをリストに格納する
def loadPages():
    cur.execute('SELECT * FROM cookpages2')
    pages = [row[0] for row in cur.fetchall()]
    return pages

#レシピの検索一覧とレシピを交互にたどってクローリングする
def getLinks(pageURL, level, pages, pageURLs):

    #深さを9までとする
    if level > 9:
        return
    

    #DelishKitchenのレシピ検索候補ページのURLをオープンする
    html = urlopen('https://delishkitchen.tv{}'.format(pageURL))
    soup = BeautifulSoup(html, 'html.parser')

    #URLオープンしたhtmlファイルからレシピのリンクを全て探す
    #それらをリストに格納する
    recipeURLs = soup.findAll('a', href=re.compile('/recipes/[0-9]*'))
    recipeURLs = [recipeURL.attrs['href'] for recipeURL in recipeURLs]

    #リストに格納したレシピをfor文で1つ1つ調べる
    for recipeURL in recipeURLs:
        if recipeURL in pages:
            continue
        
        pages.append(recipeURL)

        #レシピのURLをオープンする
        linkhtml = urlopen('https://delishkitchen.tv{}'.format(recipeURL))
        bs = BeautifulSoup(linkhtml, 'html.parser')

        #レシピのタイトル名を取得する
        try:
            recipeTitle = bs.find('p', {'class':'text-h3'}).get_text()
        except AttributeError:
            recipeTitle = ''
        
        recipeTitle += bs.find('h1', {'class':'title text-h1'}).get_text()
        recipeTitle = re.sub(r'\n|\u0020|\u3000|レシピ・作り方', '', recipeTitle)
        print(recipeTitle)

        #レシピの調理時間を取得する
        try:
            recipeTime = bs.find('div', {'class':'cooking-time-text'}).get_text()
            recipeTime = re.sub(r'調理時間|約|分|以上|半日|-|\n|\u0020', '', recipeTime)
            recipeTime = int(recipeTime)
        except AttributeError:
            recipeTime = -1
        except ValueError:
            recipeTime = -1
        
        #レシピの材料を取得する
        OrderThings = []
        for OrderThing in bs.findAll('div', {'class':'ingredient'}):
            try: #aタグから取得
                OrderThing = OrderThing.find('a').get_text()
            except AttributeError: #spanタグから取得
                OrderThing = OrderThing.find('span').get_text()
            OrderThings.append(OrderThing)
            if len(OrderThings) > 4:
                break
        
        while len(OrderThings) < 4:
            OrderThings.append('None')

        #レシピのURLとタイトルと調理時間をデータベースに格納する
        insertUrlTitle(recipeURL, recipeTitle, recipeTime, 
            OrderThings[0], OrderThings[1], OrderThings[2])

        #レシピのサイトの関連ワードのURLを全て見つける
        foodStuffLinks = bs.find('div', {'class':'content'})
        foodStuffLinks = foodStuffLinks.findAll('a', href=re.compile('/categories/[0-9]*'))
        foodStuffLinks = [foodStuffLink.attrs['href'] for foodStuffLink in foodStuffLinks]

        for foodStuffLink in foodStuffLinks:

            #一度クローリングした関連ワードのURLは無視する
            #まだクローリングしていない関連ワードのURLをpageURLリストに格納する
            if foodStuffLink in pageURLs:
                continue
            pageURLs.append(foodStuffLink)

            #上記の内容を繰り返す
            getLinks(foodStuffLink, level+1, pages, pageURLs)

#検索候補ページ(材料)を野菜からクローリングする(材料はなんでもいい)
getLinks('/categories/458', 0, loadPages(), [])
cur.close()
conn.close()