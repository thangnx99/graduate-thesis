import RPi.GPIO as GPIO
import time

OUT_LOA=21

#setup........................
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(OUT_LOA, GPIO.OUT)

def loa(t=0.5):
    GPIO.output(OUT_LOA, GPIO.HIGH)
    time.sleep(t)
    GPIO.output(OUT_LOA, GPIO.LOW)
    


