#Nhap thu vien
import numpy as np
import cv2
import time

#Cau hinh loai bo diem sang nho
kernel = np.ones((11,11), np.uint8)

def quet_re(video):
    # Lay anh
    ret, frame = video.read()
    
    (h, w, _) = frame.shape
    h1 = int(h*0.1)
    h2 = int(h*0.2)
    
    # Cat anh
    crop_img = frame[h1:h2, 0:w]

    # Chuyen ve anh xam
    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

    # Blur anh
    blur = cv2.GaussianBlur(gray,(5,5),0)

    # Tach nguong
    ret,thresh = cv2.threshold(blur,40,255,cv2.THRESH_BINARY_INV)

    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

    if thresh[int((h1-h2)/2),int(0.15*w)] == 255 :
        datatr = 1
    else: datatr = 0
    
    if thresh[int((h1-h2)/2),int(0.85*w)] == 255 :
        dataph = 1
    else: dataph = 0
    
    return datatr,dataph,thresh
