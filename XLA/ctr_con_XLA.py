#Nhap thu vien

import numpy as np
import cv2
from pyzbar import pyzbar

#font chu
font = cv2.FONT_HERSHEY_PLAIN 

#Cau hinh loai bo diem sang nho
kernel = np.ones((19,19), np.uint8)
kernel2 = np.ones((11,11), np.uint8)

def do_line(video):
    # Lay anh
    ret, frame = video.read()
    
    # Lat anh
    #frame = cv2.flip(frame,0)
    
    # Lay kich thuc anh
    (h, w, _) = frame.shape
    h1 = int(h*0.3)
    h2 = int(h*0.5)
    
    # Cat anh
    crop_img = frame[h1:h2, 0:w]

    # Chuyen ve anh xam
    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

    # Blur anh
    blur = cv2.GaussianBlur(gray,(5,5),0)

    # Tach nguong
    ret,thresh = cv2.threshold(blur,60,255,cv2.THRESH_BINARY_INV)

    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

    # Tim cacs duong vien
    contours,hierarchy = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)

    # Tim duong bao lon nhat
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)

        if M['m00'] != 0 : 

            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])

            cv2.line(crop_img,(cx,0),(cx,720),(255,0,0),1)
            cv2.line(crop_img,(0,cy),(1280,cy),(255,0,0),1)

            cv2.drawContours(crop_img, contours, -1, (0,255,0), 1)

            kct = int(w/2 - cx) #khoang cach tam, fix sai so lech 2 piex

            data = "OK"
        else:
            data = "0"
            kct = w+50

    else:
        data = "0"
        kct = w+50

    return data,kct,crop_img

def diem_re(video,min_mau,max_mau):
    check, img = video.read()#Nhap anh

    # Lay kich thuc anh
    (h, w, _) = img.shape
    h3 = int(h*0.4)
    h4 = int(h*0.6)
    
    # Cat anh
    hsv_img = img[h3:h4, 0:w]

    #Tim tron do
    hsv_img = cv2.cvtColor(hsv_img,cv2.COLOR_BGR2HSV)#chuyen sang he mau hsv
    
    mask = cv2.inRange(hsv_img, min_mau, max_mau)#Mat la khoang mau 1

    mask = cv2.medianBlur(mask,9)#Lam min loc nhieu

    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel2)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel2)#Loai bo vung sang nho

    ret,thresh = cv2.threshold(mask,127,255,0)#Nhi phan anh
    contours,hierarchy = cv2.findContours(thresh, 1, 2)#Tim cac vung sang

    S = 0
    
    for cnt in contours:
        x,y,w,h = cv2.boundingRect(cnt)#Doc cac tham so tung vung sang
        if w*h > S:
            S = w*h
            Tx = int(x + 0.5*w)
            Ty = int(y + 0.5*h)
    if S>0:
        cv2.putText(img,'X',(Tx,Ty), font, 1,(255,0,0),2,cv2.LINE_AA)
        #Viet chu
        X = 1
    else: 
        X = 0
        Tx = -1

    return X,img,Tx

def quet_QR(video):
    _ , frame = video.read()
    barcodes = pyzbar.decode(frame)
    if not barcodes : 
        huong = '0'
        barcodeData = '0'
    for barcode in barcodes:
        if barcode.type == 'QRCODE':
            (x, y, w, h) = barcode.rect
            huong = barcode.orientation
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
            barcodeData = barcode.data.decode("utf-8")
            cv2.putText(frame, 'QR', (x-10, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 0, 255), 1)

    return huong,barcodeData,frame

    
    



