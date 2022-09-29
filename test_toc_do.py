from XLA import ctr_con_XLA as xla
from module import l298
import cv2
import time
import numpy as np
import matplotlib.pyplot as plt
from dataclasses import replace

#Khoang mau nhan dien diem re
min_mau = np.array([3, 20, 20])#khoang mau  hsv min
max_mau = np.array([27, 225, 225])#khoang mau  hsv max

i=0

M = l298.MotorRobot()
speed=100

#PID

Kp = 0.3

Ki = 1.053
Kd = 0.0214
Sum = 0.0
Err = 0.0
Errlast = 0.0
n=0
Ptime2 = time.time()-0.001
pTime3 =0.0
#Setup video
video = cv2.VideoCapture(0)

X,_,Tx = xla.diem_re(video,min_mau,max_mau)
_,kct,frame = xla.do_line(video)


while True:
    i = i + 1
    if i == 1 :
        
        #Check Diem re
        X,_,Tx = xla.diem_re(video,min_mau,max_mau)
    
    if X == 0: #ko co diem re
        #Do line
        _,kct,frame = xla.do_line(video)
        #print('Cach tam: ',- kct)
        
        #PID
        n = n + 1
        Err = - kct +1
        P = Kp*Err
        
        Sum = Sum + Err
        I = Ki * Sum/n
        
        Ctime = time.time()

        D = Kd * (Err-Errlast)/(Ctime-Ptime2)
        
        Out = int(P + I + D)

        with open('Data/time.txt', mode='a',encoding = 'utf-8') as file:
            file.write(str(round(Ctime,5)).replace('.',',')+'\n')

        with open('Data/Err.txt', mode='a',encoding = 'utf-8') as file:
            file.write(str(Err).replace('.',',')+'\n')

        Errlast = Err
        Ptime2 = Ctime
                
        if speed>10 : M.move(speed=speed,turn=Out)
        else :
            M.stop()
    
    else : # Phat hien diem re       
        M.stop()
        break
    if i==6: i=0
    cv2.imshow("Image", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
video.release()
cv2.destroyAllWindows()