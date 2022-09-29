import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
Pstart = 20
Preset = 16

GPIO.setup(Pstart, GPIO.IN)
GPIO.setup(Preset, GPIO.IN)

def nut(N):
    if N == 'start': R = GPIO.input(Pstart)
    elif N == 'reset': R = GPIO.input(Preset)
    
    return R