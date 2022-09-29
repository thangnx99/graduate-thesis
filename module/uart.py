import serial  # Khai báo thưu viện serial
import time
ser = serial.Serial('/dev/ttyACM0',9600)  # Lưu ý x là số cổng USB hồi nãy bạn xem
data_left = 1

def doc_serial():
    s = ser.readline()
    data = s.decode()
    data = data.rstrip() # Loai bo “\r\n” o cuoi chuoi du lieu
    return data

def doc():

    try: data = doc_serial()
    except: data = doc_serial()
    
    while data.count('_')<5 or len(data)<22 or data[5]!='_': #Doi den khi doc du chuoi du lieu 18 ky tu
        data = doc_serial()

    ser.reset_input_buffer()
    #data_left = ser.inWaiting()
    data_tach = data.split('_')
    return(data_tach)