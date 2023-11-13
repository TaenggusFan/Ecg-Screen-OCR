# 開啟電腦Cam，每隔幾秒截圖並存入目標資料夾(Save)做後續文字擷取及ETL
import cv2
import numpy as np
import os
import time


cap = cv2.VideoCapture(0)

try:

    if not os.path.exists('Save'):
        os.makedirs('Save')

except OSError:
    print('Error: Creating directory of data')


def save_image(image, addr, num):
    address = addr + str(num) + '.jpg'
    cv2.imwrite(address, image)


index = 0
imgname = 0

while True:
    index = index + 1
    ret, frame = cap.read()
    cv2.imshow('frame', frame)
    nowtime = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime(time.time()))
    if index == 100:  # 100 = 6秒截圖一次
        imgname = imgname + 1
        if imgname >= 50:  # 最多50張後重新覆蓋 imgname = 0
            imgname = 0
        fname = str(nowtime) + '.jpg'
        cv2.imwrite('./Pic_Original/' + fname, frame)
        print(nowtime + ' 截圖完成')
        index = 0
# 延遲50ms實際相當於獲取20禎的圖像
    if cv2.waitKey(50) & 0xff == ord('a'):
        break
cap.release()
cv2.destroyAllWindows()
