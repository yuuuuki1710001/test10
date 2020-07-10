"""
    (あくまでコードは例です(担当者はコードを書き直してください))
    C3:レシピ検索部
    Date:2020/07/05
    purpose:レシピの検索一覧を取得する
"""

from urllib.request import urlopen #URLを開くためのライブラリ
from urllib.error import URLError #urllibが投げる例外ライブラリ
from bs4 import BeautifulSoup #htmlからデータを取得するためのライブラリ
import pymysql #MySQLのライブラリ
import MeCab #形態素解析ライブラリ

#MySQLに接続する(おまじない)
conn = pymysql.connect(
                    #host='172.30.27.88',
                    user='admin',
                    passwd='10pan',
                    db='cook', 
                    port=3306,
                    charset='utf8')
cur = conn.cursor()
cur.execute('USE cook')



"""
    FunctionName:   CleanWords
    Date:           2020/6/26
    Designer:       鳥居昭吾
    Function:       入力した材料名を形態素解析する
    entry:          OrderThing  --- 入力した材料名
    return:         words       --- 形態素解析した単語ら(list型)

"""
def CleanWords(OrderThing):
    m = MeCab.Tagger()
    m.parse(OrderThing)
    node = m.parseToNode(OrderThing) #単語と品詞の両方を解析する
    words = []
    hinshi = ['動詞', '名詞', '形容詞']
    while node:
        word = node.surface #単語
        pos = node.feature.split(',')[0] #品詞
        if pos in hinshi:
            words.append(word)
        node = node.next
    return words


    
"""
    FunctionName:   IngredientsInputs
    Date:           2020/07/05
    Designer:
    Function:       レシピの検索候補を取得する
    entry:          OrderThing   --- 入力した材料名
    return:         recipeTitles --- レシピの検索候補(list型)
"""
def IngredientsInputs(OrderThing, recipeTime):
    words = CleanWords(OrderThing) 
    print(words)

    #レシピ一覧を格納するリストを用意する
    recipeTitles = []

    #時間のみが入力された場合
    if OrderThing == '':
        cur.execute('SELECT * FROM cookpages WHERE recipeTime <= %s'
                'AND recipeTime != -1', (recipeTime))
        searchTitlesT1= [row[1] for row in cur.fetchall()]
        recipeTitles.extend(searchTitlesT1)
        return recipeTitles
    

    #材料が3つ入力された場合
    if len(words) == 3:
        #材料から検索
        cur.execute('SELECT * FROM cookpages WHERE OrderThing = %s'
            'AND OrderThing2 = %s'
            'AND OrderThing3 = %s',
            (words[0], words[1], words[2]))
        searchTitles = [row[1] for row in cur.fetchall()]

        cur.execute('SELECT * FROM cookpages WHERE OrderThing = %s'
            'AND OrderThing2 = %s'
            'AND OrderThing3 = %s',
            (words[1], words[2], words[0]))
        searchTitles2 = [row[1] for row in cur.fetchall()]

        cur.execute('SELECT * FROM cookpages WHERE OrderThing = %s'
            'AND OrderThing2 = %s'
            'AND OrderThing3 = %s',
            (words[2], words[0], words[1]))
        searchTitles3 = [row[1] for row in cur.fetchall()]

        recipeTitles.extend(searchTitles)
        recipeTitles.extend(searchTitles2)
        recipeTitles.extend(searchTitles3)

        #タイトルから検索
        cur.execute('SELECT * FROM cookpages')
        searchTitlesT = [row[1] for row in cur.fetchall()] #レシピタイトルを取得

        #MeCabで形態素解析したすべてのワードがレシピタイトルに含んでいる場合
        for recipeTitle in searchTitlesT:
            if (words[0] in recipeTitle) and (words[1] in recipeTitle) and (words[2] in recipeTitle):
                recipeTitles.append(recipeTitle)

        
        return recipeTitles
    
    #材料名が2つ入力された場合
    elif len(words) == 2:
        cur.execute('SELECT * FROM cookpages WHERE OrderThing = %s'
            'AND OrderThing2 = %s',
            (words[0], words[1]))
        searchTitles = [row[1] for row in cur.fetchall()]

        cur.execute('SELECT * FROM cookpages WHERE OrderThing = %s'
            'AND OrderThing2 = %s',
            (words[1], words[0]))
        searchTitles2 = [row[1] for row in cur.fetchall()]

        cur.execute('SELECT * FROM cookpages WHERE OrderThing2 = %s'
            'AND OrderThing3 = %s',
            (words[0], words[1]))
        searchTitles3 = [row[1] for row in cur.fetchall()]

        cur.execute('SELECT * FROM cookpages WHERE OrderThing2 = %s'
            'AND OrderThing3 = %s',
            (words[1], words[0]))
        searchTitles4 = [row[1] for row in cur.fetchall()]

        cur.execute('SELECT * FROM cookpages WHERE OrderThing = %s'
            'AND OrderThing3 = %s',
            (words[0], words[1]))
        searchTitles5 = [row[1] for row in cur.fetchall()]

        cur.execute('SELECT * FROM cookpages WHERE OrderThing = %s'
            'AND OrderThing3 = %s',
            (words[1], words[0]))
        searchTitles6 = [row[1] for row in cur.fetchall()]

        recipeTitles.extend(searchTitles)
        recipeTitles.extend(searchTitles2)
        recipeTitles.extend(searchTitles3)
        recipeTitles.extend(searchTitles4)
        recipeTitles.extend(searchTitles5)
        recipeTitles.extend(searchTitles6)

        
    
        #タイトルから検索
        cur.execute('SELECT * FROM cookpages')
        searchTitlesT = [row[1] for row in cur.fetchall()] #レシピタイトルを取得

        for recipeTitle in searchTitlesT: 

            #MeCabで形態素解析したすべてのワードがレシピタイトルに含んでいる場合
            if (words[0] in recipeTitle) and (words[1] in recipeTitle):
                recipeTitles.append(recipeTitle)


        return recipeTitles
    
    #材料名が1つの場合
    elif len(words) == 1:
        cur.execute('SELECT * FROM cookpages WHERE OrderThing = %s',
            (words[0]))
        searchTitles = [row[1] for row in cur.fetchall()]

        cur.execute('SELECT * FROM cookpages WHERE OrderThing2 = %s',
            (words[0]))
        searchTitles2 = [row[1] for row in cur.fetchall()]

        cur.execute('SELECT * FROM cookpages WHERE OrderThing3 = %s',
            (words[0]))
        searchTitles3 = [row[1] for row in cur.fetchall()]

        recipeTitles.extend(searchTitles)
        recipeTitles.extend(searchTitles2)
        recipeTitles.extend(searchTitles3)

        #タイトルから検索
        cur.execute('SELECT * FROM cookpages')
        searchTitlesT = [row[1] for row in cur.fetchall()]

        #MeCabで形態素解析したすべてのワードがレシピタイトルに含んでいる場合
        for recipeTitle in searchTitlesT:
            if words[0] in recipeTitle:
                recipeTitles.append(recipeTitle)

        return recipeTitles
    
    #それ以外
    else:

        #タイトルから検索
        for word in words:
            cur.execute('SELECT * FROM cookpages')
            searchTitlesT = [row[1] for row in cur.fetchall()]

            #MeCabで形態素解析したすべてのワードがレシピタイトルに含んでいる場合
            for recipeTitle in searchTitlesT:
                if word in recipeTitle:
                    recipeTitles.append(recipeTitle)

        return recipeTitles

    
#cur.close()
#conn.close()