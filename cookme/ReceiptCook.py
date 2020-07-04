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
