"""
    ReceiptCook     :   画像文字認識処理
    Date            :   2020/07/21
    Purpose         :   レシート画像から読み込まれた材料を取得
"""

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



"""
    FunctionName    :   readOrderThing
    Data            :   2020/07/21
    Designer        :   鳥居昭吾
    Function        :   レシート画像から読み込まれた材料を取得する
    Entry           :   picName     --- レシート画像のファイル名
    Return          :   searchWords --- レシート画像から読み込まれた材料(list型)
"""
def readOrderThing(picName):   
    ReceiptRead.convert(picName, CUT=True)
    # レシートデータから文字データを抽出する。出力ファイルは`output.txt`

    # あらかじめ作っておいたfood_list.txtを呼び出す。(絶対パス)
    baseDir = os.path.abspath(os.path.dirname(__file__))
    foodListFileName = os.path.join(baseDir, 'foodList.txt')
    f = open(foodListFileName, 'r', encoding="utf-8")
    data1 = f.read()
    f.close()
    lines = data1.split('\n')
    fileName = "output.txt"
    f = open(fileName,encoding="utf-8")
    data2 = f.read()
    receiptData = data2.split()
    print("read data txt is \n ",receiptData)
    # レシートから読み込んだ文字列を表示
    searchWords = []

    # 食材リストと照らし合わせてリストに照合するものがレシートのデータに存在すれば
    # その3つの食材をsearch_wordsに加える
    for word in lines:
        for receipt in receiptData:
            if word in receipt:
                searchWords.append(word)
                print("True")

    print(searchWords)
    searchWords.sort(key=len, reverse=True)
    searchWords = searchWords[:3]
    print(searchWords,"\n")
    return searchWords


