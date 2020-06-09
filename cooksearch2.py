from urllib.request import urlopen
from urllib.error import URLError
from bs4 import BeautifulSoup
import pymysql
import MeCab

#材料や調理時間を入力してからレシピ一覧を取得する
#ユースケース:レシピを検索する
conn = pymysql.connect(host='172.30.24.219', 
                    port=3306,
                    user='admin',
                    passwd='10pan',
                    db='cook',
                    charset='utf8')
cur = conn.cursor()
cur.execute('USE cook')

#MeCabで検索ワードを形態素解析する
def cleanWords(title):
    m = MeCab.Tagger()
    m.parse(title)
    node = m.parseToNode(title) #単語と品詞の両方を解析する
    words = []
    hinshi = ['動詞', '名詞', '形容詞']
    while node:
        word = node.surface #単語
        pos = node.feature.split(',')[0] #品詞
        if pos in hinshi:
            words.append(word)
        node = node.next
    return words

def selectTitle(title):
    words = cleanWords(title)
    searchTitles = []
    for word in words:
        cur.execute('SELECT * FROM cookpages')
        titles = [row[2] for row in cur.fetchall()] #pagesからタイトルをすべて取得
        #print(titles)
        for title in titles:
            if word in title:
                searchTitles.append(title)
    
    if searchTitles == []:
        return
    print(searchTitles)
    return searchTitles
    

#cur.close()
#conn.close()