from socket import MsgFlag
import l298
import GY271

M = l298.MotorRobot()

def Sang_trai(speed):

    M.move(speed=speed/2,turn=-speed/2)
    goc = GY271.HeadingAngle()
    return goc

def Sang_phai(speed):

    M.move(speed=speed/2,turn=speed/2)
    goc = GY271.HeadingAngle()
    return goc

