import numpy as np
import os
import cv2
import cookme.ReceiptRead
import matplotlib.pyplot as plt
import re
import sys
import pyocr
import pyocr.builders
picName = sys.argv[1]


cookme.ReceiptRead.convert(picName, CUT=True)
# レシートデータから文字データを抽出する。出力ファイルは`output.txt`

# あらかじめ作っておいたfood_list.txtを呼び出す。
f = open('food_list.txt')
data1 = f.read()
f.close()
lines = data1.split('\n')
fileName = "output.txt"
f = open(fileName,encoding="utf-8")
data2 = f.read()
recipeData = data2.split()
print("read data txt is \n ",recipeData)
# レシートから読み込んだ文字列を表示
searchWords = []

# 食材リストと照らし合わせてリストに照合するものがレシートのデータに存在すれば
# その3つの食材をsearch_wordsに加える
for word in lines:
    for receipt in recipeData:
        if word in receipt:
            searchWords.append(word)
            print("True")

print(searchWords)
searchWords.sort(key=len, reverse=True)
searchWords = searchWords[:3]
print(searchWords,"\n")
