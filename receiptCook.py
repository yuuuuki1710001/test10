import numpy as np
import os
import cv2
import ReceiptRead
import matplotlib.pyplot as plt
import re
import sys
import pyocr
import pyocr.builders
pic_name = sys.argv[1]


ReceiptRead.convert(pic_name, CUT=True)
# レシートデータから文字データを抽出する。出力ファイルは`output.txt`

# あらかじめ作っておいたfood_list.txtを呼び出す。
f = open('food_list.txt')
data1 = f.read()
f.close()
lines = data1.split('\n')
filename = "output.txt"
f = open(filename,encoding="utf-8")
data2 = f.read()
receipt_data = data2.split()
print("read data txt is \n ",receipt_data)
# レシートから読み込んだ文字列を表示
search_words = []

# 食材リストと照らし合わせてリストに照合するものがレシートのデータに存在すれば
# その3つの食材をsearch_wordsに加える
for word in lines:
    for receipt in receipt_data:
        if word in receipt:
            search_words.append(word)
            print("True")

print(search_words)
search_words.sort(key=len, reverse=True)
search_words = search_words[:3]
print(search_words,"\n")
"""
print("search_words is ....", search_words, "\n")
url = "https://cookpad.com/search/{:s}%E3%80%80{:s}%E3%80%80{:s}".format(search_words[0],
                                                     search_words[1],search_words[2])
# ここからスクレイピング
import requests
import lxml.html
import os
import cv2
import matplotlib.pyplot as plt


def save_image(filename, image):
    with open(filename, "wb") as fout:
        fout.write(image)

# 3つの検索ワードで検索する場合
url = "https://cookpad.com/search/{:s}%E3%80%80{:s}%E3%80%80{:s}".format(search_words[0],
                                                     search_words[1],search_words[2])
# レシピ検索のhtmlを取得
response = requests.get(url)
root = lxml.html.fromstring(response.content)
root.make_links_absolute(response.url)
url_list = []
# 検索の上位にあるレシピのurlを獲得する
for a in root.cssselect('a.recipe-title'):
    url = a.get('href')
    url_list.append(url)

response = requests.get(url_list[0])
root = lxml.html.fromstring(response.content)
recipe_title = root.cssselect("title")[0].text_content()
print(recipe_title, "\n")
ingridient_name = root.cssselect("span.name")
ingridient_amount = root.cssselect("div.ingredient_quantity")
step = root.cssselect("p.step_text")

## os.system("wget {:s} -o picture.jpg".format(src))

print("必要な材料")
for i in range(len(ingridient_name)):
    print(ingridient_name[i].text_content() + "\t" + ingridient_amount[i].text_content())
print("作り方")
for i in range(len(step)):
    print(i, ",\t",step[i].text_content())

# 画像ファイルの読み込みと表示
src = root.cssselect("#main-photo > img")[0].get('src')
src = re.findall(r'https://.+\.jpg', src)[0]
img_response = requests.get(src, timeout=10, stream=False)
name_search = re.findall(r'\/([a-zA-Z0-9:.=_-]*jpg|jpeg|JPG|JPEG)', src)
img_name = name_search[0]
save_image('./pictures/' + img_name, img_response.content)
recipe_image = cv2.imread("./pictures/"+img_name)

plt.imshow(recipe_image[:,:,::-1])

plt.show()
"""