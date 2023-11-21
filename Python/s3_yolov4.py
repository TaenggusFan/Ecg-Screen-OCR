#參考https://ithelp.ithome.com.tw/articles/10297918透過讀取訓練後權重測試框後的位置是否正確
#參考https://ithelp.ithome.com.tw/articles/10282327?sc=rss.qu
#整個流程為確認權重正確將物件偵測後的六個位置的數字分別截圖到資料夾作為後續OCR用


import cv2
import numpy as np
import os

# 讀取模型與訓練權重存放路徑
def initNet():
    CONFIG = './Yolov4/Darknet/cfg/yolov4-obj-ech.cfg' #訓練前調整的權重檔
    WEIGHT = './Yolov4/Darknet/backup/yolov4-obj-ech_last.weights' #物件偵測訓練後結果
    net = cv2.dnn.readNet(CONFIG, WEIGHT)
    model = cv2.dnn_DetectionModel(net)
    model.setInputParams(size=(416, 416), scale=1/255.0)
    model.setInputSwapRB(True)
    return model

# 物件偵測
def nnProcess(image, model):
    classes, confs, boxes = model.detect(image, 0.4, 0.1)
    return classes, confs, boxes

# 框選偵測到的物件
def drawBox(image, classes, confs, boxes):
    new_image = image.copy()
    for (classid, conf, box) in zip(classes, confs, boxes):
        x, y, w, h = box
        cv2.rectangle(new_image, (x, y), (x + w, y + h), (0, 255, 0), 3)
    return new_image

# 裁減圖片
def cut_img(image, classes, confs, boxes):
    cut_img_list = []
    for (classid, conf, box) in zip(classes, confs, boxes):
        x, y, w, h = box
        cut_img = image[y:y + h, x:x + w]
        cut_img_list.append(cut_img)
    return cut_img_list

# 儲存已完成前處理之圖檔
def saveClassify(image, output):
    cv2.imencode(ext='.jpg', img=image)[1].tofile(output)


if __name__ == '__main__':
    source = './Pic_Crop/'
    files = os.listdir(source)
    print('※ 資料夾共有 {} 張圖檔'.format(len(files)))
    print('※ 開始執行YOLOV4物件偵測...')
    model = initNet()
    success = fail = uptwo = 0
    number = 1
    for file in files:
        print(' ▼ 第{}張'.format(number))
        img = cv2.imdecode(np.fromfile(source+file, dtype=np.uint8), -1)
        classes, confs, boxes = nnProcess(img, model)
        if len(boxes) == 0:  # 如果沒偵測到字元
            fail += 1
            print('  物件偵測失敗：{}'.format(file))
        elif len(boxes) < 6:  # 如果偵測到的字元小於6 這個專案的物件有六個
            print('  物件偵測超過6個')
            box_img = drawBox(img, classes, confs, boxes)
            uptwo += 1
        else:  # 偵測=6 就開始執行裁減的動作
            # 框選後圖檔
            frame = drawBox(img, classes, confs, boxes)
            # 裁剪後圖檔
            cut = cut_img(img, classes, confs, boxes)
            # for image_name in image_names: #這邊做一紀錄，由於在上面已經有一個file的迴圈這邊再寫一個導致一個迴圈裡面所有物件偵測後的圖片一起被跑完了
            # image_path = os.path.join(image_folder, image_name)
            # img = cv2.imread(image_path)
            if len(boxes) == 0:
                print(f'物件檢測無效：{file}')
            else:
                for i, cut in enumerate(cut_img(img, classes, confs, boxes)):
                    wait_time = 1000  # 設定1秒間隔讓圖片可以完整顯示
                    # 加入預先建立好儲存每張圖片300.jpg物件偵測出來的六個位置數字的圖片，去除文件後面的.jpg，只要名稱
                    folder_name = os.path.join('./Yolov4/obj_result', file.split('.')[0])
                    # 接著依照每張圖片的名稱去建一個相對應的資料夾，名稱為300
                    os.makedirs(folder_name, exist_ok=True)
                    # 這6張物件偵測的圖片名稱會依序叫做300_1/ 300_2 ... 300/6
                    image_filename = os.path.join(
                        folder_name, f'{file}_{i + 1}.jpg')
                    cv2.imwrite(image_filename, cut)  #1.這裡依序保存6個位置才建後的圖片
                    # cv2.imshow(f'Image {i+1}', cut) #如果不想先儲存可以用imshow先檢視把上一行imwrite#不執行
                    print(f'物件儲存成功：{image_filename}')
                    cv2.waitKey(wait_time)
            success += 1
            print('  物件偵測成功：{}'.format(file))
            frameimg = './Yolov4/obj_result2/' + f'yolov4_{file}' #2.這裡是保存物件偵測後整張圖片6個框選的位置
            cv2.imwrite(frameimg, frame)  # 保存
            # cv2.imshow('img', frame)
        print('=' * 60)
        cv2.waitKey()
        number += 1
    print('※ 執行完畢 總計：成功 {} 張、失敗 {} 張'.format(success, fail))
