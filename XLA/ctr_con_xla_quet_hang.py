import cv2
from pyzbar import pyzbar

#font chu
font = cv2.FONT_HERSHEY_PLAIN 

def quet_QR_hang(video2):
    _ , frame = video2.read()
    barcodes = pyzbar.decode(frame)
    if not barcodes : 
        barcodeData = '0'
    for barcode in barcodes:
        if barcode.type == 'QRCODE':
            (x, y, w, h) = barcode.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
            barcodeData = barcode.data.decode("utf-8")
            cv2.putText(frame, 'QR', (x-10, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 0, 255), 1)

    return barcodeData,frame