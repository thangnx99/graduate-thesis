from XLA import ctr_con_XLA as xla
from module import l298
import cv2
import time
import numpy as np
from XLA import ctr_con_xla_re_xe as xlarx
from XLA import ctr_con_xla_q180 as xla180
from XLA import ctr_con_xla_quet_hang as xlaqh
from module import loa
from module import check_nut as c_n


def pid():
    
    M = l298.MotorRobot()
    
    #Toc do
    speed=0
     
    #So lan do line / quet diem re
    he_so_quet = 8 #>=4

    #Bien dem tg
    pTime = 0

    #Bien luu tinh trang hang
    Ma_hang = '00'
    mahangmax = '07'

    #data QR diem re
    data='__'

    #checkhang
    cohang=0
    cohanglast=0

    #%Pin
    pin=80

    fps=0#Khung hinh/giay

    #Khoang mau nhan dien diem re
    min_mau = np.array([3, 20, 20])#khoang mau  hsv min
    max_mau = np.array([27, 225, 225])#khoang mau  hsv max

    i=int(0)#Bien dem lan lap

    #PID
    Kp = 0.3
    Ki = 1.053
    Kd = 0.0214
    Sum = 0.0
    Err = 0.0
    Errlast = 0.0
    n=0
    Ptime2 = time.time()-0.03

    #Bien bao truoc
    DL=DL_tach=''
    che_do='0'
    che_do_last='5'
    lan_lap=0
    ok=1
    oklast=1
    loi_mat_QR=0
    

    #Setup video
    video = cv2.VideoCapture(0)
    video2 = cv2.VideoCapture(1)
    width  = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    RX = 0
    X=0

    def Quay_180(video,speed):
        datatr = dataph = -1
        gui_data_main('1',0)
        speed=int(speed*1.15)
        print('Quay 180 do nga tu')
        while datatr !=1 :
                datatr,_,thresh=xlarx.quet_re(video)
                speed,_ = doc_data_gui()
                M.move(speed=0,turn=-speed)
                cv2.imwrite('Photo/frame.jpg',thresh)
                time.sleep(0.01)
                if c_n.nut('reset') == True: break
        datagi = -1
        while datagi !=1 :
                datagi,thresh=xla180.q180(video)
                speed,_ = doc_data_gui()
                M.move(speed=0,turn=-speed)
                cv2.imwrite('Photo/frame.jpg',thresh)
                time.sleep(0.01)
                if c_n.nut('reset') == True: break
        gui_data_main('0',0)
        resetPID()

           
    def Re_xe(video,hr,speed):
        datatr,dataph,thresh=xlarx.quet_re(video)
        print('Dang re')
        speed=int(speed*1.15)
        if hr == 'tr':
            gui_data_main('2',0)
            while datatr !=1 :
                datatr,_,thresh=xlarx.quet_re(video)
                speed,_ = doc_data_gui()
                M.move(speed=speed/2,turn=-(speed/2)-5)
                cv2.imwrite('Photo/frame.jpg',thresh)
                time.sleep(0.01)
                if c_n.nut('reset') == True: break
        else: 
            gui_data_main('3',0)
            while dataph !=1 :
                _,dataph,thresh=xlarx.quet_re(video)
                speed,_ = doc_data_gui()
                M.move(speed=speed/2,turn=speed/2+5)
                cv2.imwrite('Photo/frame.jpg',thresh)
                time.sleep(0.01)
                if c_n.nut('reset') == True: break
        gui_data_main('0',0)
        resetPID()

    def Di_thang(speed):
        gui_data_main('4',0)
        print('Tiep tuc di thang')
        M.move(speed=speed,turn=0,t=0.7)
        gui_data_main('0',0)
        resetPID()
        
    def Lui_xe(speed):
        M.move(speed=-speed,turn=0,t=0.1)

    def doc_data_gui():
        DL_tach =''
        while len(DL_tach) != 2 :
            with open("Data/data_gui.txt",'r',encoding = 'utf-8') as f:
                DL = f.read()
                DL_tach = DL.split('_')
        speed = int(DL_tach[0])
        cohang = int(DL_tach[1])
        if c_n.nut('start') != True: speed = 0
        return speed,cohang

    def doc_data_gui2():
        DL_tach =''
        while len(DL_tach) != 3 :
            with open("Data/data_gui2.txt",'r',encoding = 'utf-8') as f2:
                DL = f2.read()
                DL_tach = DL.split('_')
        che_do = DL_tach[0]
        lan_lap = int(DL_tach[1])
        Ma_hang = DL_tach[2]
        return che_do,lan_lap,Ma_hang
    
    def gui_data_main(data3,vtri):
        with open('Data/data_main.txt','r+',encoding = 'utf-8') as f1:
            f1.seek(vtri,0)
            f1.write(data3)
    
    def gui_data_web(speed,ok,Ma_hang,lan_lap,che_do):
        with open('Data/data_to_web.txt', 'w') as wf2:
            wf2.write(str(speed)+'_'+str(ok)+'_'+Ma_hang+'_'+str(lan_lap)+'_'+che_do)

    def resetPID():
        global Sum,Err,Errlast,n,Ptime2
        Sum = 0.0
        Err = 0.0
        Errlast = 0.0
        n=0
        Ptime2 = time.time()-0.03
        print('Rs PID')


    while True :
        
        i = i + 1
        if che_do != '0':
            if i == 1 :
                
                #Check Diem re
                X,_,Tx = xla.diem_re(video,min_mau,max_mau)
                
                #Tinh so khung hinh tren giay
                cTime = time.time()
                fps = he_so_quet / (cTime - pTime)
                pTime = cTime

                print("FPS:",int(fps))
                i = 1
            
            if X == 0: #ko co diem re
                RX=0
                #Do line
                _,kct,frame = xla.do_line(video)
                #print('Cach tam: ',- kct)
                
                #PID
                n = n + 1
                Err = - kct + 1
                P = Kp*Err
                
                Sum = Sum + Err
                if n>1:
                    I = Ki * Sum/n
                    D = Kd * (Err-Errlast)/(time.time()-Ptime2)
                else:
                    I = 0
                    D = 0
                Out = int(P + I + D)

                Errlast = Err
                Ptime2 = time.time()
                
                #DK Dong co, loai bo loi mat line
                if abs(Err)>0.5*width: 
                    _,kct,_ = xla.do_line(video)
                    if abs(kct)>0.5*width:
                        M.stop()
                        resetPID()
                        
                if speed>50 : M.move(speed=speed,turn=Out)
                else :
                    M.stop()
                    resetPID()
                
            else : # Phat hien diem re       
                M.stop(t=0.05)
                X,_,Tx = xla.diem_re(video,min_mau,max_mau)
                if X==1:
                #Lui_xe(speed=speed)
                    for j in range (0,5):
                        huong,data,frame = xla.quet_QR(video)
                        if data != '0' : #Ktra xem co nhan dc du lieu QR hay khong
                            data = data.split('_')#tach du lieu tung line
                            print("Che do quet QR, data: ",data)
                            loa.loa(t=0.1)
                            cv2.imwrite('Photo/frame.jpg',frame)
                            M.stop(t=0.1)
                            RX = 1
                            resetPID()
                            loi_mat_QR=0
                            break
                        else : 
                            RX = 0
                            loi_mat_QR=loi_mat_QR+1

            #In FPS vao anh
            cv2.putText(frame, 'FPS: ' + str(int(fps)), (20, 20), cv2.FONT_HERSHEY_PLAIN, 1,
                        (0, 100, 255), 1)
            #luu tru anh
            if i == 2 :
                cv2.imwrite('Photo/frame.jpg',frame)

            #Den diem re nga tu chon re
            if RX == 1 and len(data)==4 : # Co du lieu QR la diem re nga tu
                X=0
                if huong == 'UP' : ih = int(0)
                elif huong == 'LEFT' : ih = int(1)
                elif huong == 'DOWN' : ih = int(2)
                elif huong == 'RIGHT' : ih = int(3)

                line_sau = data[ih].split('-')
                line_trai = data[(ih+1)%4].split('-')
                line_truoc = data[(ih+2)%4].split('-')
                line_phai = data[(ih+3)%4].split('-')

                if len(line_sau)==1 : 
                    if line_sau[0] == Ma_hang :
                         Quay_180(video,speed)
                elif int(line_sau[0])<=int(Ma_hang)<=int(line_sau[1]) :
                    Quay_180(video,speed)
                
                if len(line_trai)==1 : 
                    if line_trai[0] == Ma_hang : Re_xe(video,'tr',speed)
                elif int(line_trai[0])<=int(Ma_hang)<=int(line_trai[1]) : Re_xe(video,'tr',speed)
                
                if len(line_truoc)==1 : 
                    if line_truoc[0] == Ma_hang :
                        Di_thang(speed)
                        print('DT1')
                elif int(line_truoc[0])<=int(Ma_hang)<=int(line_truoc[1]) :
                    Di_thang(speed)
                    print('DT2')

                if len(line_phai)==1 : 
                    if line_phai[0] == Ma_hang : Re_xe(video,'ph',speed)
                elif int(line_phai[0])<=int(Ma_hang)<=int(line_phai[1]) : Re_xe(video,'ph',speed)
                loi_mat_QR=0
            if RX == 0 and X==1 : #Gap diem do ko co QR thi dung xe
                M.stop(0.1)
                if loi_mat_QR>10:
                    _,_,Tx = xla.diem_re(video,min_mau,max_mau)
                    if(Tx-(width/2))<80:
                        M.move(speed=0,turn=-90,t=0.1)
            
                    elif(Tx - width/2)>80:
                        M.move(speed=0,turn=90,t=0.1)
                    M.stop()

                
            if che_do == '1': #Che do luu kho
                #Dang o phong '00' doi nhan hang    
                if RX == 1 and data == ['00'] and cohang == 0:
                    if pin > 20 :
                        M.stop(t=0.25) #Dung xe
                    else : pass #Di sac pin
                    
                #Dang o phong '00' va da nhan hang
                if RX == 1 and data == ['00'] and cohang == 1 and Ma_hang != '00':
                    Quay_180(video,speed)
                    ok=0
                    
                #Dang tren duong line va co hang: chay binh thuong
                    
                #Den kho hang dung ma hang, Dung doi lay hang
                if RX == 1 and data[0] == Ma_hang and len(data)==1 and cohang==1:
                    M.stop(t=0.25)
                    #Doi lay hang
                    
                #Den kho hang sai ma hang, Quay 180
                if RX == 1 and data[0] != Ma_hang and data!=['00']and len(data)==1 and cohang==1:
                    print('Sai kho hang')
                    Quay_180(video,speed)
                
                #Den kho dung ma hang, Hang da dc lay di
                if RX == 1 and data != ['00'] and len(data)==1 and cohang==0:
                    M.stop(t=0.25)
                    Quay_180(video,speed)
                    Ma_hang='00' # De ve phong '00' nhan hang
                    ok=1
                    
                if i == 4 or RX == 1 :#check ma hang moi
                    if cohanglast==0 and cohang==1:
                        print('Quet ma hang')
                        gui_data_main('5',0)
                        data2='0'
                        M.stop()
                        for l in range(0,3):
                            loa.loa(t=0.1)
                            time.sleep(0.1)
                        while data2 == '0' or int(data2)>int(mahangmax) :
                            for v in range(0,10) : data2,frame = xlaqh.quet_QR_hang(video2)
                            cv2.imwrite('Photo/frame.jpg',frame)
                            if int(data2)>int(mahangmax) : print('Ma hang khong hop le')
                        Ma_hang=data2
                        for l in range(0,3):
                            loa.loa(t=0.1)
                            time.sleep(0.1)
                        gui_data_main('0',0)
                        print('Ma hang: ',data2)
                        gui_data_main(data2,2)
                        time.sleep(1)
                    if cohanglast==1 and cohang==0:
                        print('Da khong con hang')
                        M.stop(t=2)
                        Ma_hang='00'
                        print('Ma hang: ',Ma_hang)
                        gui_data_main(Ma_hang,2)   
                    cohanglast=cohang
            
            elif che_do == '2': #Che do xuat kho
                #Dang o phong '01' doi xuat hang
                if RX == 1 and data == ['01'] and cohang == 1 and Ma_hang == '01':
                    if pin > 20 :
                        M.stop(t=0.25) #Dung xe
                    #else : pass #Di sac pin
                    
                #Dang o phong '01' doi lenh lay hang
                if RX == 1 and data == ['01'] and cohang == 0 and Ma_hang == '01':
                    if pin > 20 :
                        M.stop(t=0.25) #Dung xe
                        ok=1
                    #else : pass #Di sac pin
                    
                #Dang o phong '01' da co lenh lay hang tu kho quay 180
                if RX == 1 and data[0] != Ma_hang and len(data)==1 and cohang == 0 and Ma_hang != '01':
                    if Ma_hang == '01' or int(Ma_hang)>int(mahangmax) : 
                        print('Ma hang khong hop le, thu lai')
                        Ma_hang = '01'
                    else:
                        Quay_180(video,speed)
                        ok=0
                        data='111'
                #Den kho hang dung ma hang, Dung doi nhan hang
                if RX == 1 and data[0] == Ma_hang and len(data)==1 and cohang==0:
                    M.stop(t=0.25)
                    
                #Den kho hang sai ma hang, Quay 180
                if RX == 1 and data[0] != Ma_hang and data!=['01']and len(data)==1 and cohang==0:
                    print('Sai kho hang')
                    Quay_180(video,speed)
                
                #Den kho dung ma hang, Hang da dc de len xe
                if RX == 1 and data != ['00'] and data != ['01'] and len(data)==1 and cohang==1:
                    Quay_180(video,speed)
                    Ma_hang='01' # De ve phong '01' xuat hang

            if ok==0 and oklast==1:
                if che_do == '2':
                    lan_lap=lan_lap-1
                    with open('Data/data_gui2.txt','r+',encoding = 'utf-8') as f5:
                        f5.seek(2,0)
                        f5.write(str(lan_lap))
                oklast=0
                gui_data_web(speed,ok,Ma_hang,lan_lap,che_do)


            elif ok==1 and oklast==0:
                if che_do == '2':    
                    if lan_lap==0: 
                        with open('Data/data_gui2.txt', 'w') as wf:
                            wf.write('2_0_01')
                    if lan_lap>0:
                        Ma_hang = Ma_hang_last
                oklast=1
                gui_data_web(speed,ok,Ma_hang,lan_lap,che_do)   

        if i == 3 or RX == 1 :#cap nhat speed, check hang, che do
            speed,cohang = doc_data_gui()
            che_do,_,_ = doc_data_gui2()
            if che_do == '2' and lan_lap == 0 and ok==1 :
                _,lan_lap,Ma_hang = doc_data_gui2()
                Ma_hang_last=Ma_hang
            if che_do != che_do_last:
                gui_data_main(che_do,5) 
                gui_data_web(speed,ok,Ma_hang,lan_lap,che_do)
                che_do_last = che_do            
            print('Speed : ',speed)
            print('Hang : ',cohang)
            print('Che do: ',che_do)
            print('Ma hang : ',Ma_hang)

        data='111'
        #Lap lai vong lap i    
        if i == he_so_quet :
            i = 0
            if (c_n.nut('reset') == True or che_do == '0' ):
                break
            
            

        




