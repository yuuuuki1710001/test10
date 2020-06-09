from urllib.request import urlopen
from bs4 import BeautifulSoup
import pymysql
import re

conn = pymysql.connect(host='172.30.24.219', 
                    port=3306,
                    user='admin',
                    passwd='10pan',
                    db='cook',
                    charset='utf8')
cur = conn.cursor()
cur.execute('USE cook')


def insertUrlTitle(url, title):

    #データベースに格納している内容を取得する
    cur.execute('SELECT * FROM cookpages WHERE url = %s'
        'AND title = %s', (url, title))

    #取得した数が0の場合はurlとタイトル名をデータベースに格納する
    if cur.rowcount == 0:
        cur.execute('INSERT INTO cookpages (url, title) VALUES (%s, %s)', (url, title))

        #格納した情報を保存する
        conn.commit()

def loadPages():
    cur.execute('SELECT * FROM cookpages')
    pages = [row[1] for row in cur.fetchall()]
    return pages

#クローリングのやり方は深さ優先探索である
def getLinks(PageUrl, level, pages):

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
        title = bs.find('h1').get_text()
        title = re.sub(r'\n|\u0020|\u3000', '', title)
        print(title)

        #レシピのurlとタイトルをデータベースに格納する
        insertUrlTitle(link, title)

        #レシピのサイトの関連ワードのurlを全て見つける
        foodlinks = bs.findAll('a', href=re.compile('^(/search/)((?!:).)*$'))
        foodlinks = [foodlink.attrs['href'] for foodlink in foodlinks]

        for foodlink in foodlinks:
            foodlink = foodlink.replace('/search', '')

            #既に見つけた材料(関連ワード)はクローリングしない
            if PageUrl in foodlink:
                continue

            #上記の内容を繰り返す
            getLinks(foodlink, level+1, pages)

#検索候補ページ(材料)をマグロからクローリングする(材料はなんでもいい)
getLinks('/%E3%81%BE%E3%81%90%E3%82%8D', 0, loadPages())
cur.close()
conn.close()