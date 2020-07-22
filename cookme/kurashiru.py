"""
    Kurashiru      :   レシピ情報格納処理
    Date           :   2020/07/16
    Purpose        :   レシピ情報のデータベース処理
"""

from urllib.request import urlopen
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


"""
    FunctionName    :   insertUrlTitle
    Data            :   2020/07/23
    Designer        :   野田啓介
    Function        :   レシピの情報をcookpagesテーブルに格納する
    Entry           :   recipeUrl   --- レシピのURL
                    :   recipeTitle --- レシピタイトル
                    :   recipeTime  --- 調理時間
                    :   orderThing  --- 材料
                    :   orderThing2 --- 材料
                    :   orderThing3 --- 材料
    Return          :   なし
"""
def insertUrlTitle(recipeUrl, recipeTitle, recipeTime, orderThing, orderThing2, orderThing3):

    #データベースに格納しているレシピの情報を取得する
    cur.execute('SELECT * FROM cookpages WHERE recipeURL = %s'
        'AND recipeTitle = %s'
        'AND recipeTime = %s',
        (recipeUrl, recipeTitle, recipeTime))

    #取得した数が0の場合はレシピのURL, レシピタイトル, 調理時間, 材料(3つ)をデータベースに格納する
    if cur.rowcount == 0:
        cur.execute('INSERT INTO cookpages (recipeURL, recipeTitle, recipeTime, OrderThing, OrderThing2, OrderThing3)' 
        'VALUES (%s, %s, %s, %s, %s, %s)', (recipeUrl, recipeTitle, recipeTime, orderThing, orderThing2, orderThing3))

        #格納した情報を保存する
        conn.commit()


"""
    FunctionName    :   loadPages
    Data            :   2020/07/23
    Designer        :   野田啓介
    Function        :   cookpagesテーブルに格納されているレシピのURLをリスト(pages)で格納する
    Entry           :   なし
    Return          :   pages --- cookpagesテーブルに格納されているレシピのURL(list型)
"""
def loadPages():
    cur.execute('SELECT * FROM cookpages')
    pages = [row[0] for row in cur.fetchall()]
    return pages


"""
    FunctionName    :   getLinks
    Data            :   2020/07/23
    Designer        :   野田啓介
    Function        :   レシピの情報をクローリングする
    Entry           :   pageUrl  --- 検索ワードのURL
                    :   level    --- クローリングする深さ
                    :   pages    --- cookpagesテーブルに格納されているレシピのURL(list型)
                    :   pageUrls --- クローリングする際に, 一度たどった検索ワードのURLをリストに格納する(list型)
    Return          :   なし
"""
def getLinks(pageUrl, level, pages, pageUrls):

    #クローリングする深さを9までにする
    if level > 9:
        return
    

    #Kurashiruのレシピ検索ワードのURLをオープンする
    html = urlopen('https://www.kurashiru.com{}'.format(pageUrl))
    soup = BeautifulSoup(html, 'html.parser')

    #URLオープンしたhtmlファイルからレシピのリンクを全て探す
    #それらをリスト(recipeUrls)に格納する
    recipeUrls = soup.findAll('a', href=re.compile('/recipes/'))
    recipeUrls = [recipeUrl.attrs['href'] for recipeUrl in recipeUrls]

    #リスト(recipeUrls)に格納したレシピをfor文で1つ1つ調べる
    for recipeUrl in recipeUrls:
        if recipeUrl in pages:
            continue
        
        pages.append(recipeUrl)

        #レシピのURLをオープンする
        linkHtml = urlopen('https://www.kurashiru.com{}'.format(recipeUrl))
        bs = BeautifulSoup(linkHtml, 'html.parser')

        #レシピのタイトル名を取得する
        recipeTitle = bs.find('h1').get_text()
        recipeTitle = re.sub(r'\n|レシピ・作り方', '', recipeTitle)
        print(recipeTitle)

        #レシピの調理時間を取得する
        try:
            recipeTime = bs.find('p', {'class':'cooking-time'}).get_text()
            recipeTime = re.sub(r'調理時間：|分|\n|\u0020', '', recipeTime)
            recipeTime = int(recipeTime)
        except AttributeError:
            recipeTime = -1

        #レシピの材料を取得する
        orderThings = []
        for orderThing in bs.findAll('span', {'class':'ingredient-name'}):
            orderThing = orderThing.get_text()
            orderThing = re.sub(r'〇|◎|●|○|■|□|◇|◆|△|▲|▽|▼|⊿|♪|♩|♫|♬|~', '', orderThing)
            orderThing = orderThing.strip(string.punctuation + string.whitespace)
            orderThings.append(orderThing)
        while len(orderThings) < 3:
            orderThings.append('None')

        #レシピのURL, レシピタイトル, 調理時間, 材料(3つ)をデータベースに格納する
        insertUrlTitle(recipeUrl, recipeTitle, recipeTime, 
            orderThings[0], orderThings[1], orderThings[2])

        #レシピのページの関連ワード(検索ワード)のURLを全て見つける
        orderThingUrls = bs.findAll('a', href=re.compile('/video_categories/'))
        orderThingUrls = [orderThingUrl.attrs['href'] for orderThingUrl in orderThingUrls]

        for orderThingUrl in orderThingUrls:

            #一度たどった検索ワードのURLはもうたどらない
            if orderThingUrl in pageUrls:
                continue
            pageUrls.append(orderThingUrl)

            #上記の内容を繰り返す
            getLinks(orderThingUrl, level+1, pages, pageUrls)

#今回は検索ワードを野菜からクローリングすることにする
getLinks('/video_categories/140', 0, loadPages(), [])
cur.close()
conn.close()