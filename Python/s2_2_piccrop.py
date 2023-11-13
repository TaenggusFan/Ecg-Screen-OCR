#將圖片進行截圖，所有後續物件偵測測試的範圍

#圖片讀取 https://blog.gtwang.org/programming/opencv-basic-image-read-and-write-tutorial/
#座標https://www.twblogs.net/a/5cd3b562bd9eee6726c959b4
import cv2
import numpy as np
import glob

path = "./Pic_Covert" #若原始圖檔不為jpg，需要轉檔
dirs = glob.glob(path + './*jpg')

def readPath(path):
    for i in range(len(dirs)):
        img = cv2.imread(dirs[i])
        x = 200
        y = 120
        w = 800
        h = 500
        img_cut = img[y:y+h, x:x+w]
        Img_Name = "./Pic_Crop/" + str(i) + ".jpg"
        cv2.imwrite(Img_Name, img_cut)
        #cv2.imshow('oxxostudio', img_cut)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()

if __name__ == '__main__':
    readPath(path)