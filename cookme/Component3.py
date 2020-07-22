"""
    C3      :   レシピ検索部
    Date    :   2020/07/21
    Purpose :   レシピの検索一覧を取得
"""

from urllib.request import urlopen 
from urllib.error import URLError 
from bs4 import BeautifulSoup 
import pymysql 
import re

#MySQL接続
conn = pymysql.connect(
    user    =   'root',
    passwd  =   '10pan',
    db      =   'cook',
    port    =   3306,
    charset =   'utf8'
)
cur = conn.cursor()
cur.execute('USE cook')

    
"""
    FunctionName    :   ingredientsInputs
    Date            :   2020/07/21
    Designer        :   鳥居昭吾
    Function        :   レシピの検索候補を取得
    entry           :   orderThing   --- 入力した材料名
    return          :   recipeTitles --- レシピの検索候補(list型)
"""
def ingredientsInputs(orderThing, recipeTime):
    words = re.split('[ 　]', orderThing)
    print(words)

    #レシピ一覧を格納するリストを用意する
    recipeTitles = []

    #時間のみが入力された場合
    if orderThing == '':
        cur.execute('SELECT * FROM cookpages WHERE recipeTime <= %s'
                'AND recipeTime != -1',
                (recipeTime))
        searchTitlesT1= [row[1] for row in cur.fetchall()]
        recipeTitles.extend(searchTitlesT1)
        return recipeTitles
    

    #材料が3つ入力された場合
    if len(words) == 3:
        #材料から検索
        if recipeTime == -1:
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

        else:
            cur.execute('SELECT * FROM cookpages WHERE OrderThing = %s'
                'AND OrderThing2 = %s'
                'AND OrderThing3 = %s'
                'AND recipeTime <= %s'
                'AND recipeTime != -1',
                (words[0], words[1], words[2], recipeTime))
            searchTitles = [row[1] for row in cur.fetchall()]

            cur.execute('SELECT * FROM cookpages WHERE OrderThing = %s'
                'AND OrderThing2 = %s'
                'AND OrderThing3 = %s'
                'AND recipeTime <= %s'
                'AND recipeTime != -1',
                (words[1], words[2], words[0], recipeTime))
            searchTitles2 = [row[1] for row in cur.fetchall()]

            cur.execute('SELECT * FROM cookpages WHERE OrderThing = %s'
                'AND OrderThing2 = %s'
                'AND OrderThing3 = %s'
                'AND recipeTime <= %s'
                'AND recipeTime != -1',
                (words[2], words[0], words[1], recipeTime))
            searchTitles3 = [row[1] for row in cur.fetchall()]

        recipeTitles.extend(searchTitles)
        recipeTitles.extend(searchTitles2)
        recipeTitles.extend(searchTitles3)

        #レシピタイトルから検索
        #調理時間が入力されていないとき
        if recipeTime == -1:
            cur.execute('SELECT * FROM cookpages WHERE recipeTime = -1')

        #調理時間が入力されているとき
        else:
            cur.execute('SELECT * FROM cookpages WHERE recipeTime <= %s'
                'AND recipeTime != -1', (recipeTime))
        searchTitlesT = [row[1] for row in cur.fetchall()] #レシピタイトルを取得

        #材料がレシピタイトルに含んでいる場合
        for recipeTitle in searchTitlesT:
            if (words[0] in recipeTitle) and (words[1] in recipeTitle) and (words[2] in recipeTitle):
                recipeTitles.append(recipeTitle)

        
        return recipeTitles
    
    #材料名が2つ入力された場合
    elif len(words) == 2:
        if recipeTime == -1:
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

        else:
            cur.execute('SELECT * FROM cookpages WHERE OrderThing = %s'
                'AND OrderThing2 = %s'
                'AND recipeTime <= %s'
                'AND recipeTime != -1',
                (words[0], words[1], recipeTime))
            searchTitles = [row[1] for row in cur.fetchall()]

            cur.execute('SELECT * FROM cookpages WHERE OrderThing = %s'
                'AND OrderThing2 = %s'
                'AND recipeTime <= %s'
                'AND recipeTime != -1',
                (words[1], words[0], recipeTime))
            searchTitles2 = [row[1] for row in cur.fetchall()]

            cur.execute('SELECT * FROM cookpages WHERE OrderThing2 = %s'
                'AND OrderThing3 = %s'
                'AND recipeTime <= %s'
                'AND recipeTime != -1',
                (words[0], words[1], recipeTime))
            searchTitles3 = [row[1] for row in cur.fetchall()]

            cur.execute('SELECT * FROM cookpages WHERE OrderThing2 = %s'
                'AND OrderThing3 = %s'
                'AND recipeTime <= %s'
                'AND recipeTime != -1',
                (words[1], words[0], recipeTime))
            searchTitles4 = [row[1] for row in cur.fetchall()]

            cur.execute('SELECT * FROM cookpages WHERE OrderThing = %s'
                'AND OrderThing3 = %s'
                'AND recipeTime <= %s'
                'AND recipeTime != -1',
                (words[0], words[1], recipeTime))
            searchTitles5 = [row[1] for row in cur.fetchall()]

            cur.execute('SELECT * FROM cookpages WHERE OrderThing = %s'
                'AND OrderThing3 = %s'
                'AND recipeTime <= %s'
                'AND recipeTime != -1',
                (words[1], words[0], recipeTime))
            searchTitles6 = [row[1] for row in cur.fetchall()]

        recipeTitles.extend(searchTitles)
        recipeTitles.extend(searchTitles2)
        recipeTitles.extend(searchTitles3)
        recipeTitles.extend(searchTitles4)
        recipeTitles.extend(searchTitles5)
        recipeTitles.extend(searchTitles6)

        #レシピタイトルから検索
        #調理時間が入力されていないとき
        if recipeTime == -1:
            cur.execute('SELECT * FROM cookpages WHERE recipeTime = -1')

        #調理時間が入力されているとき
        else:
            cur.execute('SELECT * FROM cookpages WHERE recipeTime <= %s'
                'AND recipeTime != -1', (recipeTime))
        searchTitlesT = [row[1] for row in cur.fetchall()] #レシピタイトルを取得

        for recipeTitle in searchTitlesT: 

            #材料がレシピタイトルに含んでいる場合
            if (words[0] in recipeTitle) and (words[1] in recipeTitle):
                recipeTitles.append(recipeTitle)

        return recipeTitles
    
    #材料名が1つの場合
    elif len(words) == 1:
        if recipeTime == -1:
            cur.execute('SELECT * FROM cookpages WHERE OrderThing = %s',
                (words[0]))
            searchTitles = [row[1] for row in cur.fetchall()]

            cur.execute('SELECT * FROM cookpages WHERE OrderThing2 = %s',
                (words[0]))
            searchTitles2 = [row[1] for row in cur.fetchall()]

            cur.execute('SELECT * FROM cookpages WHERE OrderThing3 = %s',
                (words[0]))
            searchTitles3 = [row[1] for row in cur.fetchall()]

        else:
            cur.execute('SELECT * FROM cookpages WHERE OrderThing = %s'
                'AND recipeTime <= %s'
                'AND recipeTime != -1',
                (words[0], recipeTime))
            searchTitles = [row[1] for row in cur.fetchall()]

            cur.execute('SELECT * FROM cookpages WHERE OrderThing2 = %s'
                'AND recipeTime <= %s'
                'AND recipeTime != -1',
                (words[0], recipeTime))
            searchTitles2 = [row[1] for row in cur.fetchall()]

            cur.execute('SELECT * FROM cookpages WHERE OrderThing3 = %s'
                'AND recipeTime <= %s'
                'AND recipeTime != -1',
                (words[0], recipeTime))
            searchTitles3 = [row[1] for row in cur.fetchall()]

        recipeTitles.extend(searchTitles)
        recipeTitles.extend(searchTitles2)
        recipeTitles.extend(searchTitles3)

        #レシピタイトルから検索
        #調理時間が入力されていないとき
        if recipeTime == -1:
            cur.execute('SELECT * FROM cookpages WHERE recipeTime = -1')

        #調理時間が入力されているとき
        else:
            cur.execute('SELECT * FROM cookpages WHERE recipeTime <= %s'
                'AND recipeTime != -1', (recipeTime))
        searchTitlesT = [row[1] for row in cur.fetchall()]

        #材料がレシピタイトルに含んでいる場合
        for recipeTitle in searchTitlesT:
            if words[0] in recipeTitle:
                recipeTitles.append(recipeTitle)

        return recipeTitles
    
    #それ以外
    else:

        #レシピタイトルから検索
        for word in words:

            #調理時間が入力されていないとき
            if recipeTime == -1:
                cur.execute('SELECT * FROM cookpages WHERE recipeTime = -1')

            #調理時間が入力されているとき
            else:
                cur.execute('SELECT * FROM cookpages WHERE recipeTime <= %s'
                    'AND recipeTime != -1', (recipeTime))
            searchTitlesT = [row[1] for row in cur.fetchall()]

            #材料がレシピタイトルに含んでいる場合
            for recipeTitle in searchTitlesT:
                if word in recipeTitle:
                    recipeTitles.append(recipeTitle)

        return recipeTitles
