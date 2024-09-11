import pytesseract
import cv2
import os
import matplotlib.pyplot as plt


# 指定 tesseract.exe 的路徑
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# 定義圖片檔案的路徑
file_paths = [
    "./Yolov4/obj-result3/0_1.jpg"
    #"./Yolov4/obj-result3/0_2.jpg",
    #"./Yolov4/obj-result3/0_3.jpg",
    #"./Yolov4/obj-result3/0_4.jpg",
    #"./Yolov4/obj-result3/0_5.jpg",
    #"./Yolov4/obj-result3/0_6.jpg"
]

# 初始化空的結果列表
results = []

# 迴圈處理每張圖片
for file_path in file_paths:
    # 使用 OpenCV 讀取圖片
    # 讀取圖片
    img = cv2.imread(file_path)

    # 轉換為灰度圖像
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    plt.figure(figsize=(10, 6))
    plt.subplot(231), plt.imshow(gray, cmap='gray'), plt.title('Gray Image')

    # 使用高斯模糊來減少雜訊
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    plt.subplot(232), plt.imshow(blurred, cmap='gray'), plt.title('Blurred Image')

    # 使用Canny邊緣檢測強調數字的邊緣
    edges = cv2.Canny(blurred, 50, 150)
    plt.subplot(233), plt.imshow(edges, cmap='gray'), plt.title('Edges Detected')

    # 使用膨脹操作來加強邊緣
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    dilated = cv2.dilate(edges, kernel, iterations=1)
    plt.subplot(234), plt.imshow(dilated, cmap='gray'), plt.title('Dilated Edges')

    # 進行自適應二值化處理
    binary_img = cv2.adaptiveThreshold(dilated, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    plt.subplot(235), plt.imshow(binary_img, cmap='gray'), plt.title('Adaptive Threshold')

    # 反轉二值化圖像
    inverted_img = cv2.bitwise_not(binary_img)
    plt.subplot(236), plt.imshow(inverted_img, cmap='gray'), plt.title('Inverted Image')

    plt.tight_layout()
    plt.show()

    # 設置白名單僅允許數字 0-9
    #custom_config = r'--oem 3 --psm 8 -c tessedit_char_whitelist=0123456789'

    # 使用 Tesseract 進行 OCR
    #text = pytesseract.image_to_string(inverted_img, config=custom_config)

    # 輸出辨識結果
    #print(f"OCR result: {text.strip()}")

    # 等待按鍵事件並關閉視窗
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

# 顯示所有結果
#for result in results:
#    print(f"File: {result[0]}, OCR Text: {result[1]}")
