#分別對s3_yolov4輸出的各張圖片六個物件偵測後之結果進行ocr

import cv2
import pytesseract
import os
import pandas as pd
from IPython.display import display
import csv

# 設定Tesseract的路徑
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


source_folder = './Yolov4/obj-result'
# 獲取PIC_Crop路徑下的所有子資料夾
subfolders = [f.path for f in os.scandir(source_folder) if f.is_dir()]

df_list = []

for subfolder in subfolders:
    #print(f'子文件夾: {subfolder}')

    image_files = [f.path for f in os.scandir(subfolder) if f.is_file(
    ) and f.name.lower().endswith(('.jpg', '.jpeg', '.png'))]

    #text_file = open(f'{subfolder}.txt', 'w', encoding='utf-8')

 
    for image_file in image_files:
        #print(f'子文件夾: {subfolder}')

        image = cv2.imread(image_file)
        text = pytesseract.image_to_string(image, lang='eng')
        entry = {'文件': image_file, '辨識結果': text}
        df_list.append(entry) 
        # text_file.write(f'記事本: {image_file}\n')
        # text_file.write(f'辨識記事本:\n{text}\n')
        # text_file.write('=' * 40 + '\n')   #這裡先不儲存，只print結果是否有成功，調整順利後載儲存
        #cv2.imshow('Image', image)
        #cv2.waitKey(1000)  # 每隔一秒確保圖片能完整顯示
        #df.to_csv('./OCR/ocr_results.csv', index=False, encoding='utf-8')
    # 關閉記事本
    #text_file.close()
df = pd.DataFrame(df_list)
print(df)
# 關閉所有imshow的圖片
cv2.destroyAllWindows()
