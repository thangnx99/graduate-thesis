from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import tkinter as tk
import cv2
import PIL.Image, PIL.ImageTk
from time import sleep
from threading import Thread
import RPi.GPIO as GPIO
from module import l298
from module import uart
import numpy as np
import time
import os.path
from PIL import ImageTk, Image

#Setup xử lý ảnh -------------
    
#Khoang mau nhan dien diem re
min_mau = np.array([3, 20, 20])#khoang mau  hsv min
max_mau = np.array([27, 225, 225])#khoang mau  hsv max

speed=0

#Bien dem tg
pTime = 0

fps=0

i=int(0)

data_tach='0_0_0_0_0_0'
    
font1 = ('Helvetica', 20,"bold")
font2 = ("Helvetica", 15,"bold")
font3 = ("Helvetica", 11,"bold")
a=730
b=100
# Setups ---------------------

def toc_do_dong_co(var):
    global speed
    speed = int(var)

window = Tk()
window.title("Tkinter GUI")

try :
    frame = cv2.imread('Photo/frame.jpg')
    (canvas_h, canvas_w, _) = frame.shape
except :
    exit()
canvas = Canvas(window, width = canvas_w, height= canvas_h*5 )



label_tocdo=tk.Label(window,text="Tốc độ động cơ :",font=font2).place(x=a,y=b+290)
var=DoubleVar()

scale_tocdodongco= tk.Scale(window,variable=var,command=toc_do_dong_co,orient=HORIZONTAL,length=150).place(x=a+170,y=b+270)
label_tocdo=tk.Label(window,text='%',font=font2).place(x=a+330,y=b+290)

label_doam1 = tk.Label(window,text="Độ ẩm :", font=font2).place(x=a,y=b)
label_nhietdo1 = tk.Label(window,text="Nhiệt độ :", font=font2).place(x=a,y=b+60)
label_trangthaiden1 = tk.Label(window,text="Trạng thái đèn :", font=font2).place(x=a+200,y=b)
label_checkhang = tk.Label(window,text="Hàng :", font=font2).place(x=a,y=b-60)
label_mahang = tk.Label(window,text="Mã phòng đích :", font=font2).place(x=a+200,y=b-60)
label_pin1 = tk.Label(window,text="Pin :", font=font2).place(x=a+220,y=b+60)
label_canhbaokhoangcach1 = tk.Label(window,text="Cong suat dong co :", font=font2).place(x=a,y=b+120)
label_fps = tk.Label(window,text="FPS GUI :",font=font2).place(x=60,y=b+550)

#nhiet_do2
lab_nhietdo2=tk.Label(window,text="0",width=8,bg='light yellow',font=font2)
lab_nhietdo2.place(x=a+100,y=b+60)
#do am2
label_doam2 = tk.Label(window,text = "1",width=8,bg='light yellow',font=font2)
label_doam2.place(x=a+90,y=b)
#trang thai den2
label_trangthaiden2 = tk.Label(window,text="2" ,width=8,bg='light yellow',font=font2)
label_trangthaiden2.place(x=a+360,y=b)
#checkhang2
label_checkhang2 = tk.Label(window,text="2" ,width=10,bg='light yellow',font=font2)
label_checkhang2.place(x=a+80,y=b-60)
#mã hàng
label_mahang2 = tk.Label(window,text="2" ,width=8,bg='light yellow',font=font2)
label_mahang2.place(x=a+370,y=b-60)
#pin2
label_pin2 = tk.Label(window,text="3" ,width=8,bg='light yellow',font=font2)
label_pin2.place(x=a+280,y=b+60)
#khoang cach2
label_canhbaokhoangcach2 = tk.Label(window,text='4',width=8,bg='light yellow',font=font2)
label_canhbaokhoangcach2.place(x=a+270,y=b+120)
#fps2
label_fps2 = tk.Label(window,text='',width=8,bg='light yellow',font=font2)
label_fps2.place(x=170,y=b+550)

img_phai  = Image.open("Photo/phai.png")
img_phai = img_phai.resize((100, 100), Image.ANTIALIAS)
photo_phai=ImageTk.PhotoImage(img_phai)
lab_phai=Label(window,image=photo_phai)


img_tren = img_phai.rotate(90)
photo_tren=ImageTk.PhotoImage(img_tren)
lab_tren=Label(window,image=photo_tren)
#lab_tren.place(x=a+200,y=b+400)

img_trai = img_phai.rotate(180)
photo_trai=ImageTk.PhotoImage(img_trai)
lab_trai=Label(window,image=photo_trai)


img_duoi = img_phai.rotate(-90)
photo_duoi=ImageTk.PhotoImage(img_duoi)
lab_duoi=Label(window,image=photo_duoi)

img_doline  = Image.open("Photo/doline.png")
img_doline = img_doline.resize((100, 100), Image.ANTIALIAS)
photo_doline=ImageTk.PhotoImage(img_doline)
lab_doline=Label(window,image=photo_doline)

img_qr  = Image.open("Photo/QR.png")
img_qr = img_qr.resize((100, 100), Image.ANTIALIAS)
photo_qr =ImageTk.PhotoImage(img_qr)
lab_qr =Label(window,image=photo_qr)

img_handle  = Image.open("Photo/handle.png")
img_handle = img_handle.resize((100, 100), Image.ANTIALIAS)
photo_handle =ImageTk.PhotoImage(img_handle)
lab_handle =Label(window,image=photo_handle)

imglock  = Image.open("Photo/lock.png")
imglock = imglock.resize((100, 100), Image.ANTIALIAS)
photolock=ImageTk.PhotoImage(imglock)


lablock=Label(window,image=photolock)



tk.Label(window, text="Trạng thái hoạt động :",font=font2).place(x=a,y=b+180)
label_chedo=tk.Label(window, text="Lưu kho",font=font2,width=18,bg='light yellow')
label_chedo.place(x=a+250,y=b+180)


button_lock=tk.Button(window, )

m=0
mlast=1
Ma_hang='00'
che_do='0'
speed2=1
def doc_data():
    DL_tach =''
    while len(DL_tach) != 3 :
        with open("Data/data_main.txt",'r',encoding = 'utf-8') as f:
            DL = f.read()
            DL_tach = DL.split('|')
    m = int(DL_tach[0])
    Ma_hang = DL_tach[1]
    che_do = DL_tach[2]
    return m,Ma_hang,che_do

def forget():
    lablock.place_forget()
    lab_duoi.place_forget()
    lab_tren.place_forget()
    lab_phai.place_forget()
    lab_trai.place_forget()
    lab_handle.place_forget()
    lab_doline.place_forget()
    lab_qr.place_forget()
    
def handle():
    forget()
    lab_handle.place(x=a+200,y=b+400)
    
def doline(m):
    if m==1:
        forget()
        lab_duoi.place(x=a+200,y=b+400)
    elif m == 2:
        forget()
        lab_trai.place(x=a+200,y=b+400)      
    elif m == 3:
        forget()
        lab_phai.place(x=a+200,y=b+400)
    elif m == 4:
        forget()
        lab_tren.place(x=a+200,y=b+400)
    elif m == 0:
        forget()
        lab_doline.place(x=a+200,y=b+400)
    elif m == 5:
        forget()
        lab_qr.place(x=a+200,y=b+400)





def update_frame():
    global canvas, photo, bw, count, speed, pTime, fps, i, data_tach, frame, m, Ma_hang, mlast,che_do,pin,speed2

    i = i + 1
    
    try: frame = cv2.imread('Photo/frame.jpg')
    except : pass
    try:
        while (type(frame) is not np.ndarray):       
            frame = cv2.imread('Photo/frame.jpg')
    except : pass
    
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Ressize
    frame = cv2.resize(frame, dsize=None, fx=1, fy=1)
    # Convert hanh image TK
    photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    # Show
    (h, w, _) = frame.shape
    if h < 350:
        canvas.place(x= 60,y= 150)
    else:
        canvas.place(x= 60,y= 50) 
    canvas.create_image(0,0, image = photo, anchor=tk.NW)
            
    if i==1 :
        try : data_tach = uart.doc()
        except : pass

    label_doam2.config(text=data_tach[0] +' %')
    lab_nhietdo2.config(text=data_tach[1]+ ' °C')
    if data_tach[2]=='1' : den2='Bật'
    else : den2='Tắt'
    label_trangthaiden2.config(text=den2)
    try: pin = (int((float(data_tach[3]) - 11)/0.02))
    except: pass
    if pin<0: pin = 0
    elif pin>100 : pin = 100
    label_pin2.config(text=(str(pin)) + ' %')
    if data_tach[5]=='1' : cohang2='Có hàng'
    else : cohang2='Không có'
    label_checkhang2.config(text=cohang2)
    label_fps2.config(text = int(fps))
    if Ma_hang != '00' : label_mahang2.config(text = Ma_hang)
    else : label_mahang2.config(text = 'Không')
    if speed != speed2:
        speed=50 + int(50*(speed/100))
        speed2=speed
        label_canhbaokhoangcach2.config(text=str(speed)+ ' %')
    with open('Data/data_gui.txt', 'w') as wf:
        wf.write(str(speed)+'_'+data_tach[5])
    
    if i==2:
        m,Ma_hang,che_do = doc_data()
        if mlast != m :
            if che_do == "1" or che_do == "2":
                doline(m)
            elif che_do =="0":
                handle()
        mlast = m
    
    if i==3:
        if che_do == "0":
            label_chedo.config(text='Điều khiển bằng tay')
        elif che_do == "1":
            label_chedo.config(text='Lưu kho')
        elif che_do == "2":
            label_chedo.config(text='Xuất kho')
    
    if i==6 :
        i=0
        #Hien thi so khung hinh tren giay
        cTime = time.time()
        fps = 6 / (cTime - pTime)
        pTime = cTime
    
        
        
        
    window.after(1,update_frame)
 
update_frame()

window.geometry('1280x720')
window.mainloop()




