from sqlalchemy import true
from web_server import create_app
import threading
from time import sleep


host_name = "192.168.137.90"
port = 5200

app = create_app()



if 1:#__name__ == '__main__':
    try:
        #threading.Thread(target=gui, daemon=True).start()
        app.run(host=host_name, port=port, debug=True, use_reloader=False)
        #threading.Thread(target=lambda: app.run(host=host_name, port=port, debug=True, use_reloader=False)).start()

        #f = open("data/test.txt", "r")
    except:
        print("Something went wrong")
    else:
        print("Nothing went wrong")
        
        #print(f.read())
        while true:
            sleep(1)
