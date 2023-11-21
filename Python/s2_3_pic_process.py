#圖片灰階處裡 針對圖片性質愈線處理或物件偵測裁剪後再處裡
import cv2
import numpy as np
import glob

image_path = ".\Pic_Crop"
dirs = glob.glob(image_path + './*jpg')


def Gray(image_path):
    for i in range(len(dirs)):
        image = cv2.imread(dirs[i])
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #灰階方式1
        #gray = cv2.cvtColor(image, 7) #灰階方式2
        #invert = 255 - gray 
        gray2 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 7)
        #ImgN = ".\\Pic_gray\\" + "gray" + str(i) + ".jpg"
        #cv2.imwrite(ImgN, invert)
        cv2.imshow('oxxostudio', gray2)

        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == '__main__':
    Gray(image_path)
