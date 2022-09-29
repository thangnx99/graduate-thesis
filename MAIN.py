import threading
import PID
from module import check_nut as c_n
import time
from web_server import create_app

che_do='0'

#Reset Data
with open('Data/data_gui2.txt', 'w') as wf:
    wf.write('0_0_01')

with open('Data/data_main.txt', 'w') as wf1:
    wf1.write('0|00|0')

class ThreadPID(threading.Thread):
   def __init__(self):
      threading.Thread.__init__(self)
   def run(self):
          print("Bat dau luong")
          PID.pid()

def doc_data_gui2():
    DL_tach =''
    while len(DL_tach) != 3 :
        with open("Data/data_gui2.txt",'r',encoding = 'utf-8') as f2:
            DL = f2.read()
            DL_tach = DL.split('_')
    che_do = DL_tach[0]
    return che_do
# web-------------------------------------------
# from web_server import create_app
# host_name = "192.168.1.170"
# app = create_app()
# ----------------------------------------------

luong1 = ThreadPID()
luong1.start()
# 
# if __name__ == '__main__':
#    app.run(host=host_name, debug=True, use_reloader=False)
while True:
    luong1.join()
    che_do=doc_data_gui2()
    while che_do == '0':
        che_do=doc_data_gui2()
        print('che do bang tay')
        time.sleep(0.5)
    print('reset')
    luong1.run()

    time.sleep(1)
      
        

