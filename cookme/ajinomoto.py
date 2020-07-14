from urllib.request import urlopen
from http.client import InvalidURL
from bs4 import BeautifulSoup
import pymysql
import re
import string

conn = pymysql.connect(
                    user='root',
                    passwd='10pan',
                    db='cook', 
                    port=3306,
                    charset='utf8')
cur = conn.cursor()
cur.execute('USE cook')


def insertUrlTitle(recipeURL, recipeTitle, recipeTime, OrderThing, OrderThing2, OrderThing3):

    #テーブルに格納している内容を取得する
    cur.execute('SELECT * FROM cookpages2 WHERE recipeURL = %s'
        'AND recipeTitle = %s'
        'AND recipeTime = %s', 
        (recipeURL, recipeTitle, recipeTime))

    #取得した数が0の場合はURLとタイトル名と調理時間と材料をデータベースに格納する
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

    #深さを19までとする
    if level > 29:
        return

    pageURL = bytes(pageURL, 'utf-8')
    pageURL = pageURL.decode('ascii', 'ignore')
    
    #レシピ大百科のレシピ検索候補ページのURLをオープンする
    try:
        html = urlopen('https://park.ajinomoto.co.jp/recipe{}'.format(pageURL))
    except InvalidURL:
        return
    soup = BeautifulSoup(html, 'html.parser')

    #URLオープンしたhtmlファイルからレシピのリンクを全て探す
    #それらをリストに格納する
    recipeURLs = soup.findAll('a', href=re.compile('/card/'))
    recipeURLs = [recipeURL.attrs['href'].replace('https://park.ajinomoto.co.jp/recipe', '') 
                    for recipeURL in recipeURLs]

    #リストに格納したレシピをfor文で1つ1つ調べる
    for recipeURL in recipeURLs:
        if recipeURL in pages:
            continue
        
        pages.append(recipeURL)

        #レシピのURLをオープンする
        linkhtml = urlopen('https://park.ajinomoto.co.jp/recipe{}'.format(recipeURL))
        bs = BeautifulSoup(linkhtml, 'html.parser')

        #レシピのタイトル名を取得する
        recipeTitle = bs.find('div', {'class':'recipeTitleAreaType02'}).find('span').get_text()
        print(recipeTitle)

        #レシピの調理時間を取得する
        recipeTime = bs.find('div', {'class':'inTime'}).find('strong').get_text()
        recipeTime = int(recipeTime)
        
        #レシピの材料を取得する
        OrderThings = []
        for OrderThing in bs.findAll('dt', {'class': ''}): 
            OrderThing = OrderThing.get_text()
            OrderThing = OrderThing.strip(string.punctuation + string.whitespace)
            OrderThings.append(OrderThing) #材料名を取得
            if len(OrderThings) > 4:
                break
        
        while len(OrderThings) < 4:
            OrderThings.append('None')

        #レシピのURLとタイトルと調理時間と材料をデータベースに格納する
        insertUrlTitle(recipeURL, recipeTitle, recipeTime, 
            OrderThings[0], OrderThings[1], OrderThings[2])

        #レシピのサイトの関連ワードのURLを全て見つける
        foodStuffLinks = bs.findAll('a', href=re.compile('/search/'))
        foodStuffLinks = [foodStuffLink.attrs['href'].replace('https://park.ajinomoto.co.jp/recipe', '') + '&tab=pop&o=300'
                            for foodStuffLink in foodStuffLinks]

        for foodStuffLink in foodStuffLinks:

            #一度クローリングした関連ワードのURLは無視する
            #まだクローリングしていない関連ワードのURLをpageURLリストに格納する
            if foodStuffLink in pageURLs:
                continue
            pageURLs.append(foodStuffLink)

            #上記の内容を繰り返す
            getLinks(foodStuffLink, level+1, pages, pageURLs)

#検索候補ページ(材料)を牛肉からクローリングする(材料はなんでもいい)
getLinks('/search/?search_word=%E7%89%9B%E8%82%89&tab=pop&o=300', 0, loadPages(), [])
cur.close()
conn.close()