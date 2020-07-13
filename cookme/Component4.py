"""
    C4:レシピ表示部
    Date:2020/07/07
    purpose:レシピの材料と調理時間と作り方を取得する
"""

from urllib.request import urlopen
from urllib.error import URLError
from bs4 import BeautifulSoup
import pymysql
import re

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
    FunctionName:   selectURL
    Date:           2020/07/07
    Designer:       野田 啓介
    Function:       レシピのURLを返す
    entry:          recipeTitle       --- レシピのタイトル名(str型)
    return:         cur.fetchone()[0] --- レシピのURL(str型)

"""
def selectURL(recipeTitle):
    #cookpagesから検索するレシピのURLを取得する
    cur.execute('SELECT recipeURL FROM cookpages WHERE recipeTitle = %s', (recipeTitle))
    return cur.fetchone()[0]




"""
    FunctionName:   recipeDisplay
    Date:           2020/07/07
    Designer:       野田 啓介, 續 
    Function:       レシピの材料と調理時間と作り方を返す
    entry:          recipeTitle       --- レシピのタイトル名(str型)
    return:         cur.fetchone()[0] --- レシピのURL(str型)

"""
def recipeDisplay(recipeTitle):
    recipeURL = selectURL(recipeTitle)
    print(recipeURL)

    #クラシル
    if re.search(r'^/recipes/([a-f])+|(-)+', recipeURL):
        html = urlopen('https://www.kurashiru.com{}'.format(recipeURL))
        soup = BeautifulSoup(html, 'html.parser')

        #材料
        OrderThing = ''
        for Stuff, quantity in zip(soup.findAll('span', {'class':'ingredient-name'}),
            soup.findAll('span', {'class':'ingredient-quantity-amount'})):
            OrderThing += Stuff.get_text() + ' ' + quantity.get_text() + '   '

        #調理時間
        cur.execute('SELECT recipeTime FROM cookpages WHERE recipeTitle = %s', 
                (recipeTitle))
        recipeTime = cur.fetchone()[0]

        #作り方
        recipeToCook = ''
        for recipe in soup.findAll('span', {'class':'content'}):
            recipeToCook += recipe.get_text()

        #材料と作り方を返す
        return OrderThing, recipeTime, recipeToCook

    #cookpad
    elif re.search(r'^/recipe/', recipeURL):
        html = urlopen('https://cookpad.com{}'.format(recipeURL))
        soup = BeautifulSoup(html, 'html.parser')

        #材料
        Stuff = soup.findAll('div', {'class':'ingredient_row'})
        OrderThing = ''
        for stuff in Stuff:
            for foodstu, quan in zip(stuff.findAll('div', {'class':'ingredient_name'}), 
                stuff.findAll('div', {'class':'ingredient_quantity amount'})):
                foodstuffText = foodstu.get_text().replace('\n', '')
                #print(foodstuffText + ' ' + quan.get_text())
                OrderThing += foodstuffText + ' ' + quan.get_text() + '   '

        #調理時間(-1)
        cur.execute('SELECT recipeTime FROM cookpages WHERE recipeTitle = %s', 
                (recipeTitle))
        recipeTime = cur.fetchone()[0]

        #作り方
        recipeToCook = ''
        for recipe in soup.findAll('p', {'class':'step_text'}):
            recipeToCook += recipe.get_text()
        
        #材料と作り方を返す
        return OrderThing, recipeTime, recipeToCook
    
    #DelishKitchen
    elif re.search(r'^/recipes/([0-9])+', recipeURL):
        html = urlopen('https://delishkitchen.tv{}'.format(recipeURL))
        soup = BeautifulSoup(html, 'html.parser')

        #材料
        OrderThing = ''
        for Stuff in soup.findAll('div', {'class':'ingredient'}):
            OrderThing += Stuff.get_text()

        #調理時間
        cur.execute('SELECT recipeTime FROM cookpages WHERE recipeTitle = %s', 
                (recipeTitle))
        recipeTime = cur.fetchone()[0]
        
        #作り方
        
        recipeToCook = ''
        for recipe in soup.findAll('div', {'class':'step-text-wrap'}):
            recipeToCook += recipe.get_text()

        #材料と作り方を返す
        return OrderThing, recipeTime, recipeToCook

    #レシピ大百科
    else:
        html = urlopen('https://park.ajinomoto.co.jp/recipe{}'.format(recipeURL))
        soup = BeautifulSoup(html, 'html.parser')

        #材料
        OrderThing = ''
        for Stuff, Quantity in zip(soup.findAll('dt'), soup.findAll('dd')):
            OrderThing += Stuff.get_text() + ' ' +  Quantity.get_text() + ' '

        #調理時間
        cur.execute('SELECT recipeTime FROM cookpages WHERE recipeTitle = %s', 
                (recipeTitle))
        recipeTime = cur.fetchone()[0]
        
        #作り方
        recipeToCook = ''
        for recipe in soup.findAll('div', {'class':'txt numberTxt'}):
            recipeToCook += recipe.get_text()

        #材料と作り方を返す
        return OrderThing, recipeTime, recipeToCook

