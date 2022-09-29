from tracemalloc import stop
import RPi.GPIO as GPIO
from time import sleep


HZ = 10000


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


class Motor():
    def __init__(self, in1, in2):
        self.in1 = in1
        self.in2 = in2
        GPIO.setup(self.in1, GPIO.OUT)
        GPIO.setup(self.in2, GPIO.OUT)
        self.in1_pwm = GPIO.PWM(self.in1, HZ)
        self.in2_pwm = GPIO.PWM(self.in2, HZ)
        self.in1_pwm.start(0)
        self.in2_pwm.start(0)

    def moveF(self, speed=50, t=0):
        self.in1_pwm.ChangeDutyCycle(0)
        self.in2_pwm.ChangeDutyCycle(speed)
        sleep(t)

    def moveB(self, speed=50, t=0):
        self.in1_pwm.ChangeDutyCycle(speed)
        self.in2_pwm.ChangeDutyCycle(0)
        sleep(t)
        
    def stop(self, t=0):
        self.in1_pwm.ChangeDutyCycle(0)
        self.in2_pwm.ChangeDutyCycle(0)
        sleep(t)
        
class Motor2():
    def __init__(self, in1, in2):
        self.in1 = in1
        self.in2 = in2
        GPIO.setup(self.in1, GPIO.OUT)
        GPIO.setup(self.in2, GPIO.OUT)

    def moveF(self, t=0):
        GPIO.output(self.in1,GPIO.LOW)
        GPIO.output(self.in2,GPIO.HIGH)
        sleep(t)

    def moveB(self, t=0):
        GPIO.output(self.in1,GPIO.HIGH)
        GPIO.output(self.in2,GPIO.LOW)
        sleep(t)
        
    def stop(self, t=0):
        GPIO.output(self.in1,GPIO.LOW)
        GPIO.output(self.in2,GPIO.LOW)
        sleep(t)









class MotorRobot():
    def __init__(self, in1=17, in2=27, in3=22, in4=23):
        self.in1 = in1
        self.in2 = in2
        self.in3 = in3
        self.in4 = in4

        GPIO.setup(self.in1, GPIO.OUT)
        GPIO.setup(self.in2, GPIO.OUT)
        GPIO.setup(self.in3, GPIO.OUT)
        GPIO.setup(self.in4, GPIO.OUT)

        self.in1 = GPIO.PWM(self.in1, HZ)
        self.in2 = GPIO.PWM(self.in2, HZ)
        self.in3 = GPIO.PWM(self.in3, HZ)
        self.in4 = GPIO.PWM(self.in4, HZ)

        self.in1.start(0)
        self.in2.start(0)
        self.in3.start(0)
        self.in4.start(0)
    
    def move(self, speed=50, turn=0, t=0):
        leftSpeed = speed - turn
        rightSpeed = speed + turn

        if leftSpeed > 100 : leftSpeed = 100
        elif leftSpeed < -100 : leftSpeed = -100
        if rightSpeed > 100 : rightSpeed = 100
        elif rightSpeed < -100 : rightSpeed = -100

        if rightSpeed > 0 :
            self.in1.ChangeDutyCycle(0)
            self.in2.ChangeDutyCycle(rightSpeed)
        else:
            self.in1.ChangeDutyCycle(abs(rightSpeed))
            self.in2.ChangeDutyCycle(0)
        if leftSpeed > 0 :
            self.in3.ChangeDutyCycle(0)
            self.in4.ChangeDutyCycle(leftSpeed)
        else:
            self.in3.ChangeDutyCycle(abs(leftSpeed))
            self.in4.ChangeDutyCycle(0)
        sleep(t)
        
    
    def stop(self, t=0):
        self.in1.ChangeDutyCycle(0)
        self.in2.ChangeDutyCycle(0)
        self.in3.ChangeDutyCycle(0)
        self.in4.ChangeDutyCycle(0)
        sleep(t)