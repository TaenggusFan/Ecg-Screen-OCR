import cv2
import pytesseract
import os
import pandas as pd

# 設定Tesseract的路徑
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# 設定圖片的來源資料夾
source_folder = './Yolov4/obj-result'

# 獲取資料夾下所有子資料夾的路徑
subfolders = [f.path for f in os.scandir(source_folder) if f.is_dir()]

df_list = []

# 執行每個子資料夾
for subfolder in subfolders:
    # 獲取子資料夾中的所有圖片文件
    image_files = [f.path for f in os.scandir(subfolder) if f.is_file() and f.name.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    # 確保每個資料夾中有6個圖片
    if len(image_files) < 6:
        print(f"資料夾 {subfolder} 中圖片數量不足6張，請檢查！")
        continue

    # 按照固定順序存儲每個資料夾的數據
    ocr_results = {'資料夾名稱': os.path.basename(subfolder), 'HR': None, 'SPO2': None, 'PR': None, 'SBP': None, 'DBP': None, 'MAP': None}

    # 對6個圖片進行OCR識別
    for i, image_file in enumerate(sorted(image_files)[:6]):  # 僅對前6張圖片進行OCR，並確保圖片排序一致
        # 使用 OpenCV 讀取圖片
        img = cv2.imread(image_file)
        # 轉換為灰度圖像
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 使用高斯模糊來減少雜訊
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        # 使用Canny邊緣檢測強調數字的邊緣
        edges = cv2.Canny(blurred, 50, 150)
        # 使用膨脹操作來加強邊緣
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        dilated = cv2.dilate(edges, kernel, iterations=1)
        # 進行自適應二值化處理
        binary_img = cv2.adaptiveThreshold(dilated, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        # 反轉二值化圖像
        inverted_img = cv2.bitwise_not(binary_img)

        # 設置白名單僅允許數字 0-9
        custom_config = r'--oem 3 --psm 8 -c tessedit_char_whitelist=0123456789'
        text = pytesseract.image_to_string(inverted_img, config=custom_config).strip()

        # 按順序將OCR結果存儲到對應的欄位
        if i == 0:
            ocr_results['HR'] = text
        elif i == 1:
            ocr_results['SPO2'] = text
        elif i == 2:
            ocr_results['PR'] = text
        elif i == 3:
            ocr_results['SBP'] = text
        elif i == 4:
            ocr_results['DBP'] = text
        elif i == 5:
            ocr_results['MAP'] = text

    # 將結果添加到列表中
    df_list.append(ocr_results)

# 將所有結果存儲到DataFrame
df = pd.DataFrame(df_list)

# 顯示DataFrame
print(df)
