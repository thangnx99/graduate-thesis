#Nhap thu vien
import numpy as np
import cv2
import time

#Cau hinh loai bo diem sang nho
kernel = np.ones((5,5), np.uint8)

def q180(video):
    # Lay anh
    ret, frame = video.read()
    
    (h, w, _) = frame.shape
    h1 = int(h*0.9)
    h2 = int(h)
    
    # Cat anh
    crop_img = frame[h1:h2, 0:w]

    # Chuyen ve anh xam
    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

    # Blur anh
    blur = cv2.GaussianBlur(gray,(5,5),0)

    # Tach nguong
    ret,thresh = cv2.threshold(blur,80,255,cv2.THRESH_BINARY_INV)

    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

    if thresh[int((h1-h2)*0.3),int(0.5*w)] == 255 :
        datagi = 1
    else: datagi = 0
    
    return datagi,thresh

