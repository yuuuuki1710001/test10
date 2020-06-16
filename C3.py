#入力した材料や調理時間の情報を取得して，レシピ一覧を取得する
#C3:レシピ検索部

from urllib.request import urlopen #URLを開くためのライブラリ
from urllib.error import URLError #urllibが投げる例外ライブラリ
from bs4 import BeautifulSoup #htmlからデータを取得するためのライブラリ
import pymysql #MySQLのライブラリ
import MeCab #形態素解析ライブラリ

#MySQLに接続する(おまじない)
conn = pymysql.connect(
                    user='root',
                    passwd='10pan',
                    db='cook', 
                    port=3306,
                    charset='utf8')
cur = conn.cursor()
cur.execute('USE cook')

#MeCabで入力した材料名を形態素解析する
def cleanWords(recipeTitle):
    m = MeCab.Tagger()
    m.parse(recipeTitle)
    node = m.parseToNode(recipeTitle) #単語と品詞の両方を解析する
    words = []
    hinshi = ['動詞', '名詞', '形容詞']
    while node:
        word = node.surface #単語
        pos = node.feature.split(',')[0] #品詞
        if pos in hinshi:
            words.append(word)
        node = node.next
    return words

#レシピ一覧を取得する
def selectTitle(recipeTitle):
    words = cleanWords(recipeTitle)

    #レシピ一覧を格納するリストを用意する
    searchTitles = []

    for word in words:

        #cookpagesの情報をすべて取得してからrecipeTitleだけをリストに格納する
        cur.execute('SELECT * FROM cookpages')
        recipeTitles = [row[1] for row in cur.fetchall()] 


        #レシピタイトルに、入力した材料名が含まれているかどうかを調べる
        #含まれている場合は、レシピ一覧のリストにそのレシピタイトルを追加する
        for recipeTitle in recipeTitles:
            if word in recipeTitle:
                searchTitles.append(recipeTitle)
    
    if searchTitles == []:
        return
    print(searchTitles)

    #レシピ一覧を返す
    return searchTitles
    

#cur.close()
#conn.close()