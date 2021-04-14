import sys, time
import RPi.GPIO as GPIO

RED_PIN = 11
GREEN_PIN = 13
BLUE_PIN = 15

GPIO.setmode(GPIO.BOARD)
GPIO.setup(RED_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)
GPIO.setup(BLUE_PIN, GPIO.OUT)

def turn_on(color):
    if color == 'red':
        GPIO.output(RED_PIN, True)
    elif color == 'green':
        GPIO.output(GREEN_PIN,True)
    elif color == 'blue':
        GPIO.output(BLUE_PIN, True)

def turn_off(color):
    if color == 'red':
        GPIO.output(RED_PIN, GPIO.LOW)
    elif color == 'green':
        GPIO.output(GREEN_PIN, GPIO.LOW)
    elif color == 'blue':
        GPIO.output(BLUE_PIN, GPIO.LOW)

def turn_off_all():    
    GPIO.output(RED_PIN, GPIO.LOW)
    GPIO.output(GREEN_PIN, GPIO.LOW)
    GPIO.output(BLUE_PIN, GPIO.LOW)

def blink(color, num):
    for i in range(num):
        turn_on(color)
        time.sleep(1)
        turn_off(color)

def run():
    num = 0
    while True:
        num = num % 3
        blink(num)
        num += 1
    GPIO.cleanup()

if __name__ == "__main__":
    run()