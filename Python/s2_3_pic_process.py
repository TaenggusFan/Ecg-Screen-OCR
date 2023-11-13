import cv2
import numpy as np
import glob

image_path = ".\Pic_Crop"
dirs = glob.glob(image_path + './*jpg')


def Gray(image_path):
    for i in range(len(dirs)):
        image = cv2.imread(dirs[i])
        # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.cvtColor(image, 7)
        invert = 255 - gray
        # gray2 = cv2.adaptiveThreshold(invert, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 7)
        # invert = 255 - thresh
        # ImgN = ".\\gray\\" + "gray" + str(i) + ".jpeg"
        # cv2.imwrite(ImgN, invert)
        cv2.imshow('oxxostudio', invert)

        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == '__main__':
    Gray(image_path)
