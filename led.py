import sys, time
import RPi.GPIO as GPIO

RED_PIN = 11
GREEN_PIN = 13
BLUE_PIN = 15

GPIO.setmode(GPIO.BOARD)
GPIO.setup(RED_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)
GPIO.setup(BLUE_PIN, GPIO.OUT)

def turn_on(num):
    if num == 0:
        GPIO.output(RED_PIN, True)
    elif num == 1:
        GPIO.output(GREEN_PIN,True)
    elif num == 2:
        GPIO.output(BLUE_PIN, True)

def turn_off(num):
    if num == 0:
        GPIO.output(RED_PIN, GPIO.LOW)
    elif num == 1:
        GPIO.output(GREEN_PIN, GPIO.LOW)
    elif num == 2:
        GPIO.output(BLUE_PIN, GPIO.LOW)

def blink(num):
    turn_on(num)
    time.sleep(1)
    turn_off(num)

if __name__ == "__main__":
    num = 0
    while True:
        num = num % 3
        blink(num)
        num += 1
    GPIO.cleanup()