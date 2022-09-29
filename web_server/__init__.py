import time
from flask import Flask, render_template, jsonify, request
from flask_basicauth import BasicAuth
from module import uart 



def check():
    print("CHECK WEB_SERVER !")

def doc_data_web():
    DL_tach =''
    while len(DL_tach) != 5 :
        with open("Data/data_to_web.txt",'r',encoding = 'utf-8') as f:
            DL = f.read()
            DL_tach = DL.split('_')
    speed = int(DL_tach[0])
    ok = int(DL_tach[1])
    Ma_hang = DL_tach[2]
    lan_lap = int(DL_tach[3])
    che_do = DL_tach[4]
    return speed,ok,Ma_hang,lan_lap,che_do

def create_app():
    app = Flask(__name__)

    app.config['BASIC_AUTH_USERNAME'] = 'admin'
    app.config['BASIC_AUTH_PASSWORD'] = 'admin'
    app.config['BASIC_AUTH_FORCE'] = True

    basic_auth = BasicAuth(app)

    @app.route('/')
    @app.route('/home')
    def index():
        return render_template('index.html')


    #-----------------------------------------------------------------
    # trang web cập nhật dữ liệu cảm biến ---------------------------------------------
    #-----------------------------------------------------------------
    @app.route('/_data-sensor')
    def data_sensor():
        global data
        try: data = uart.doc()
        except:
            time.sleep(0.05)
            data = uart.doc()
        finally: pass
        speed,_,_,_,_=doc_data_web()
        # Get humi and temp data --------------------------
        humi = data[0]
        temp = data[1]
        # Get light data----------------------------------
        light = int(data[2])
        if light == 0: lamp = "Tắt"
        else : lamp = "Bật"
        # Get pin data------------------------------------
        pin = int( (float(data[3]) - 11) / 0.02)
        if pin <= 0 : pin = 0
        if pin >= 100 : pin = 100
        # Get speed data-------------------------------
        distance = int((speed - 50)*100/50)
        if distance<0: distance=0
        # Get goods data----------------------------------
        goods = int(data[5])
        if goods == 1: hasgoods = "Có"
        else : hasgoods = "Không có"
        # return json------------------------------------
        return jsonify(
            temp=temp,
            humi=humi, 
            lamp=lamp, 
            pin=pin, 
            distance=distance, 
            hasgoods=hasgoods
        )

    # sensor page ------------------------------------------------------------
    @app.route('/sensor')
    def sensor():
        temp = "lấy giá trị nhiệt độ"
        humi = "lấy giá trị độ ẩm"
        lamp = "lấy giá trị độ ẩm"
        pin = "lấy giá trị độ ẩm"
        distance = "lấy giá trị độ ẩm"
        hasgoods = "lấy giá trị độ ẩm"
        return render_template('sensor.html', temp=temp, humi=humi, lamp=lamp, pin=pin, distance=distance, hasgoods=hasgoods)






    #-----------------------------------------------------------------
    # trang web xử lý điều khiển xe bằng tay-------------------------------------------------------------------------------
    #-----------------------------------------------------------------
    
    # thiết lập động cơ
    from module import l298
    motor1 = l298.Motor2(17,27)
    motor2 = l298.Motor2(22,23)

    # định tuyến trang web xử lý điều khiển xe bằng tay----------------------------------------------------
    @app.route('/_data-control')
    def data_control():
        _,ok,_,lan_lap,che_do=doc_data_web()
        isControl = bool(ok and not(lan_lap))
        if ok and che_do!= '0' and lan_lap == 0 :
            with open('Data/data_gui2.txt', 'r+',encoding = 'utf-8') as f1:
                f1.seek(0,0)
                f1.write('0')
        # return json-----------------------------------
        return jsonify(isControl=isControl)

    @app.route('/control')
    def control():
        return render_template('control.html')

    @app.route('/up')
    def up():
        print("up")
        motor1.moveF()
        motor2.moveF()
        return render_template('control.html')

    @app.route('/back')
    def back():
        print("back")
        motor1.moveB()
        motor2.moveB()
        return render_template('control.html')

    @app.route('/turn-left')
    def turn_left():
        print("turn left")
        motor1.moveF()
        motor2.moveB()
        return render_template('control.html')

    @app.route('/turn-right')
    def turn_right():
        print("turn right")
        motor1.moveB()
        motor2.moveF()
        return render_template('control.html')

    @app.route('/stop')
    def stop():
        print("stop")
        motor1.stop()
        motor2.stop()
        return render_template('control.html')





    #-----------------------------------------------------------------
    # định tuyến trang web quản lý xuất kho-------------------------------------------------------------------------
    #-----------------------------------------------------------------
    @app.route('/_data-export')
    def data_export():
        _,ok,Ma_hang,lan_lap,che_do = doc_data_web()
        count = lan_lap
        index = Ma_hang
        isDelivery = bool (not(ok and lan_lap == 0))
        # đây là biến ok, để xem xe có đang bận hay không
        isExport = bool(ok or che_do == '2')
        # return json----------------
        return jsonify(
            count=count, 
            index=index, 
            isDelivery=isDelivery,
            isExport=isExport)

    @app.route('/export', methods=["POST","GET"])
    def export():
        if request.method == "POST":
            Ma_hang = request.form["Ma_hang"]
            So_luong = request.form["So_luong"]
            with open('Data/data_gui2.txt', 'w') as wf:
                wf.write('2_'+So_luong+'_'+Ma_hang)
        return render_template('export.html')




    #-----------------------------------------------------------------
    # định tuyến trang web quản lý nhập kho-------------------------------------------------------------------------
    #-----------------------------------------------------------------
    @app.route('/_data-import')
    def data_import():
        _,ok,Ma_hang,lan_lap,che_do = doc_data_web()
        if Ma_hang == '00': Ma_hang = 'Không'
        hasGoods = bool(not(ok))
        # đây là biến ok, để xem xe có đang bận hay không
        isImport = bool(che_do == '1')
        if ok and che_do!= '1' and lan_lap == 0 :
            with open('Data/data_gui2.txt', 'r+',encoding = 'utf-8') as f1:
                f1.seek(0,0)
                f1.write('1')
        # return json----------------
        return jsonify(
            Ma_hang=Ma_hang,
            hasGoods=hasGoods,
            isImport=isImport)

    @app.route('/import')
    def _import():
        return render_template('import.html')





    return app