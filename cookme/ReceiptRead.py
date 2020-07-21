import numpy as np
import os
import glob
import matplotlib.pyplot as plt
import cv2
import pyocr 
import pyocr.builders



"""
    FunctionName    :   transformBy4
    Data            :   2020/07/21
    Designer        :   鳥居昭吾
    Function        :   透視変換行列を使って切り抜く
    Entry           :   img                   --- レシート画像
    Return          :   cv2.warpPerspective() --- 透視変換行列
"""
def transformBy4(img, points):
    points = points[np.argsort(points, axis=0)[:, 1]]
# yが小さいもの順に並び替え。
    top = points[np.argsort(points[:2], axis=0)[:, 0]]
# 前半二つは四角形の上。xで並び替えると左右も分かる。
    bottom = points[2:][np.argsort(points[2:], axis=0)[:, 0]]
# 後半二つは四角形の下。xで並び替え。
    points = np.vstack((top, bottom))
# 分離した二つを再結合。

    width = (np.abs(points[0][0]-points[1][0]) +
             np.abs(points[2][0]-points[3][0]))/2.0
    height = (np.abs(points[0][1]-points[2][1]) +
              np.abs(points[1][1]-points[3][1]))/2.0
    width = int(width)
    height = int(height)
    points2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
    points1 = np.float32(points)
    M = cv2.getPerspectiveTransform(points1, points2)
# 変換前の座標と変換後の座標の対応を渡すと、透視変換行列を作ってくれる。
    return cv2.warpPerspective(img, M, (width, height))  # 透視変換行列を使って切り抜く。
# matplotlibで正常に画像が表示できるための関数。（モノクロ画像に対して）



"""
    FunctionName    :   contEdge
    Data            :   2020/07/21
    Designer        :   鳥居昭吾
    Function        :   エッジを取り除く
    Entry           :   im     --- レシート画像
    Return          :   imRect --- 長方形の形に抜き取る
"""
def contEdge(im, fileName):
    imSize = im.shape[0] * im.shape[1]
    imGray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(fileName + '_gray.jpg', imGray)
    print(fileName + '_gray.jpg')
    imBlur = cv2.fastNlMeansDenoising(imGray)  # 画像のノイズを取り除く
    imTh = cv2.threshold(imBlur, 127, 255, cv2.THRESH_BINARY)
    # 2値化をする
    imTh = cv2.adaptiveThreshold(imBlur, 255, cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY, 15, 5)
    # im_th = cv2.Canny(im_blur, 50, 200)
    thFileName = "{:s}_th.jpg".format(fileName)
    # 2値化させた画像を表示させる。
    #show_img(im_th)
    print(thFileName)
    # 画像の保存
    cv2.imwrite(thFileName, imTh)
    print(fileName + '_th.jpg')
    #img, 
    cnts, hierarchy = cv2.findContours(imTh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # 輪郭の抽出
    # 輪郭画像、輪郭、階層情報の順に並んでいる。
    cnts.sort(key=cv2.contourArea, reverse=True)
    # 抽出された輪郭の面積が大きい順にソートをかける
    cnt = cnts[1]
    img=0
    img = cv2.drawContours(img, [cnt], -1, (0, 255, 0), 3)
    cv2.imwrite(fileName+"_drawcont.jpg", img)
    imLine = im.copy()
    warp = None
    flag = 1
    # 以下のループで抽出された輪郭を描画する
    for c in cnts[1:]:
        arclen = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02*arclen, True)
    # 輪郭を少ない点で表現（臨界点は0.02*arclen)
        if len(approx) == 4:
            cv2.drawContours(imLine, [approx], -1, (0, 0, 255), 2)
            if flag:  # 1番面積が大きいものがレシートの輪郭だと考えられるのでその輪郭情報を保存
                warp = approx.copy()
                flag = 0
        else:
            cv2.drawContours(imLine, [approx], -1, (0, 255, 0), 2)
        for pos in approx:
            cv2.circle(imLine, tuple(pos[0]), 4, (255, 0, 0))
    # レシートと思われる輪郭の面積を算出。
    # 正しくレシートの輪郭を認識できないことがあるため、元の画像に対してある一定以上の大きさでないとトリミングをしないようにした。
    area = cv2.contourArea(warp)
    print("area = ", area)
    if area > imSize//5:
        print("now cutting....")
        imRect = transformBy4(im, warp[:, 0, :])
        cv2.imwrite(fileName + '_rect.jpg', imRect)
    else:
        return im
    # 切り取った画像の表示
    plt.figure()
    plt.imshow(imLine)
    cv2.imwrite(fileName + '_line.jpg', imLine)
    print("warp = \n", warp[:, 0, :])
    print(fileName + '_rect.jp')
    return imRect



"""
    FunctionName    :   convert
    Data            :   2020/07/21
    Designer        :   鳥居昭吾
    Function        :   レシート画像から文字データを抽出するS
    Entry           :   fileName   --- レシート画像のファイル名
                        capture    --- キャプチャ
                        CUT        --- レシートの形に抜き取っている
    Return          :   output.txt --- レシート画像から読み込まれた文字を格納するテキストファイル
"""
def convert(fileName=None, capture=False, CUT=False):
    if fileName == None and capture == False:
        pass
    elif fileName :

        #絶対パス
        baseDir = os.path.abspath(os.path.dirname(__file__))
        fileName = os.path.join(baseDir, fileName)
        im = cv2.imread(fileName)
        
    fileName = fileName[:-4]
    # 拡張子を取り除いた形で記録する
    if CUT:
        im = contEdge(im, fileName)
    imRectGray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    print(fileName+'_rect_gray.jpg')
    imRectBlur = cv2.fastNlMeansDenoising(imRectGray)
    imRectTh = cv2.adaptiveThreshold(imRectBlur, 255,
                                       cv2.ADAPTIVE_THRESH_MEAN_C,
                                       cv2.THRESH_BINARY, 63, 20)

    rectThFileName = "{:s}_rect_th.jpg".format(fileName)
    cv2.imwrite(rectThFileName, imRectTh)
    print(rectThFileName)
#    show_img(im_rect_th)
# 既存のoutput.txtファイルが存在すればそれを消去して新たにoutput.txtを作成
    if glob.glob('output.txt'):
        os.remove('output.txt')
#tesseractによる画像の文字認識
    rectThFileName = "{:s}_rect_th.jpg".format(fileName)
    os.system("tesseract {:s} output -l jpn".format(rectThFileName))
