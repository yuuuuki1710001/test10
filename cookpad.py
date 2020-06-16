from urllib.request import urlopen
from bs4 import BeautifulSoup
import pymysql
import re

conn = pymysql.connect(
                    user='root',
                    passwd='10pan',
                    db='cook', 
                    port=3306,
                    charset='utf8')
cur = conn.cursor()
cur.execute('USE cook')


def insertUrlTitle(recipeURL, recipeTitle):

    #データベースに格納している内容を取得する
    cur.execute('SELECT * FROM cookpages WHERE recipeURL = %s'
        'AND recipeTitle = %s', (recipeURL, recipeTitle))

    #取得した数が0の場合はurlとタイトル名をデータベースに格納する
    if cur.rowcount == 0:
        recipeTime = -1
        cur.execute('INSERT INTO cookpages (recipeURL, recipeTitle, recipeTime) VALUES (%s, %s, %s)', (recipeURL, recipeTitle, recipeTime))

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
    links = soup.findAll('a', href=re.compile('/recipe/([0-9])*$'))
    links = [link.attrs['href'] for link in links]

    #リストに格納したレシピをfor文で1つ1つ調べる
    for link in links:
        if link in pages:
            continue
        
        pages.append(link)

        #レシピのurlをオープンする
        linkhtml = urlopen('https://cookpad.com{}'.format(link))
        bs = BeautifulSoup(linkhtml, 'html.parser')

        #レシピのタイトル名を取得する
        recipeTitle = bs.find('h1').get_text()
        recipeTitle = re.sub(r'\n|\u0020|\u3000', '', recipeTitle)
        print(recipeTitle)

        #レシピのurlとタイトルをデータベースに格納する
        insertUrlTitle(link, recipeTitle)

        #レシピのサイトの関連ワードのurlを全て見つける
        foodStuffLinks = bs.findAll('a', href=re.compile('^(/search/)((?!:).)*$'))
        foodStuffLinks = [foodStuffLink.attrs['href'] for foodStuffLink in foodStuffLinks]


        for foodStuffLink in foodStuffLinks:
            foodStuffLink = foodStuffLink.replace('/search', '')
            if foodStuffLink in pageURLs:
                continue
            pageURLs.append(foodStuffLink)

            #上記の内容を繰り返す
            getLinks(foodStuffLink, level+1, pages, pageURLs)
        
        

#検索候補ページ(材料)を生湯葉からクローリングする(材料はなんでもいい)
getLinks('/%E7%94%9F%E6%B9%AF%E8%91%89', 0, loadPages(), [])
cur.close()
conn.close()