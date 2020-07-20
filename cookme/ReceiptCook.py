import numpy as np
import os
import cv2
import matplotlib.pyplot as plt
import re
import sys
import pyocr
import pyocr.builders
from cookme import ReceiptRead
#pic_name = sys.argv[1]

def ReadOrderThing(pic_name):   
    ReceiptRead.convert(pic_name, CUT=True)
    # レシートデータから文字データを抽出する。出力ファイルは`output.txt`

    # あらかじめ作っておいたfood_list.txtを呼び出す。(絶対パス)
    basedir = os.path.abspath(os.path.dirname(__file__))
    foodListFileName = os.path.join(basedir, 'food_list.txt')
    f = open(foodListFileName, 'r', encoding="utf-8")
    data1 = f.read()
    f.close()
    lines = data1.split('\n')
    filename = "output.txt"
    f = open(filename,encoding="utf-8")
    data2 = f.read()
    receipt_data = data2.split()
    print("read data txt is \n ",receipt_data)
    # レシートから読み込んだ文字列を表示
    SearchWords = []

    # 食材リストと照らし合わせてリストに照合するものがレシートのデータに存在すれば
    # その3つの食材をsearch_wordsに加える
    for word in lines:
        for receipt in receipt_data:
            if word in receipt:
                SearchWords.append(word)
                print("True")

    print(SearchWords)
    SearchWords.sort(key=len, reverse=True)
    SearchWords = SearchWords[:3]
    print(SearchWords,"\n")
    return SearchWords

#ReadOrderThing(pic_name)
