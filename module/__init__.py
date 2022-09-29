def check():
    print("CHECK MODULE !")

def initMotorWeb():
    from module import l298
    motor1 = l298.Motor2(17,27)
    motor2 = l298.Motor2(22,23)