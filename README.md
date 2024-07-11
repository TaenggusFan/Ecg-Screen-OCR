# 資料分析專案名稱

【**運用光學字元辨識(OCR)擷取生命監護儀圖片中各項數值存入資料庫**】

公司部門剛好提到想要架個攝影機在電力面板前面，透過定時截圖並保存，文字擷取上面的數字，進行後續資料視覺化。
配合徒手打造數據分析應用案例課程，故決定自己做做看。

## 專案概述

以攝影機監控生命監護儀，定時擷取一張圖片並保存，接著使用 OCR 擷取圖片各項數值(心跳、呼吸頻率及血壓等)儲存至資料庫，整個流程將使用 Airflow 進行自動化排程
因機密問題無法實際透過攝影機拍攝公司電力面板之圖片，訓練之圖片將直接使用 Kaggle 的圖片集。《以攝影機監控生命監護儀，定時擷取一張圖片並保存》這一段流程會另找標的 Demo 出來)

## 專案結構

一、專案流程  
流程 1.圖片取得 : 攝影機監控生命監護儀，定時擷取一張圖片並保存(圖片取得會以 Kaggle 圖片集取代)  
流程 2.圖片處理 : 圖片裁減及轉檔  
流程 3.物件偵測 : 使用 YOLOv4 進行物減偵測，將專案所需要的六個位置之數值框選後另存圖片  
流程 4.OCR : OCR 文字

二、專案資料夾及檔案說明  
**\專案\PIC_Original**  
原始圖片集  
**\專案\PIC_Crop**  
裁剪後儲放 (後續進入物件偵測會複製到\專案\darknet\build\darknet\x64\data\obj 供訓練)  
**\專案\Python**  
各流程所需 py 程式碼  
s1_capture.py - 上述流程 1 攝影機定時截圖保存  
s2_1_convertojpg.py - 上述流程 2 為了物件偵測方便，圖片集格式若不是 jpg 要轉檔  
s2_2_piccrop.py - 上述流程 2 將圖片裁減，增加後續圖片偵測出來的大小以利 OCR 辨識  
s3_yolov4.py - 上述流程 3 將訓練出來的權重及結果套用到每張圖片(如下圖)  
![Yolov4訓練結果](https://github.com/TaenggusFan/Ecg-Screen-OCR/blob/main/Yolov4/Yolov4%E8%A8%93%E7%B7%B4%E7%B5%90%E6%9E%9C.png?raw=true)
接著將 6 個框選出來的數字位置分別截圖(如下圖)  
![image](https://github.com/TaenggusFan/Ecg-Screen-OCR/blob/main/OCR/OCR_Result2.png?raw=true)  
s4.ocr.py - 流程 4 將每張圖檔的 6 個位置分別另存後，各別進行 OCR  
**\專案\Yolov4**  
物件偵測所需權重檔  
Darknet - 依照自身訓練修改參數  
obj-result - 每張圖的 6 個位置數字各別裁減儲存位置  
obj-result2 - 查看每張圖片套用訓練後權重是否可正常框選 6 個位置的數字  
**\專案\OCR**  
後續存放 OCR 出來的結果，目前只用 df.dataframe show 出來，待改善辨識率後修改

## 安裝與使用方法

詳細環境配置及操作皆會按照專案結構之流程各別紀錄說明  
流程 1.圖片取得  
流程 2.圖片處理  
流程 3.物件偵測  
物件偵測需進行前期環境建置，完成後進入訓練  
[環境配置](https://medium.com/@u357ps8633/%E7%89%A9%E4%BB%B6%E5%81%B5%E6%B8%AC-yolov4-darknet-cd6ce95321b4)
[實際訓練](https://medium.com/@u357ps8633/%E7%89%A9%E4%BB%B6%E5%81%B5%E6%B8%AC-yolov4-darknet-%E8%A8%93%E7%B7%B4-76679163964c)  
訓練後測試  
訓練後依照權重進行測試，檢查框選6個位置是否正確，後續再將框選的位置裁剪後另存
  
物件偵測後會將單張圖片  
流程 4.OCR  
目前 OCR 出來的辨識率沒有很好，一張圖片 6 個位置只有 2 個數字有辨識出來專案目前成果 OCR 辨識率不高  
![image](https://github.com/TaenggusFan/Ecg-Screen-OCR/blob/main/OCR/OCR_Result.png?raw=true)  
流程 5.ETL
MongoDB

## 資料收集

流程 1.圖片取得
Kaggle Dataset 取代定時拍攝截圖
