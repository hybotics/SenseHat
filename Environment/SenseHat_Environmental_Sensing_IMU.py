#!/usr/bin/env python3
from sense_hat import SenseHat
from time import sleep

#    Set up colors
RED			 =	(255, 0, 0)
GREEN		 =	(0, 255, 0)
BLUE		 =	(0, 0, 255)
BLACK		 =	(0, 0, 0)
WHITE		 =	(255, 255, 255)

COBALT_BLUE  =  (0, 0, 100)
CYAN		 =	(0, 255, 255)
MAGENTA      =	(255, 0, 255)
ORANGE       =  (145, 75, 0)
YELLOW       =	(255, 255, 0)

USE_SENSE_DISPLAY = True

#    Default settings
MINUTE_SECONDS = 60

DEFAULT_BACKGROUND_COLOR = COBALT_BLUE
DEFAULT_TEXT_COLOR = YELLOW
DEFAULT_SCROLL_SPEED = 0.085
DEFAULT_DELAY_SEC = 2.60
DEFAULT_READING_INTERVAL_MIN = 5.0

MAX_LOOPS = 10
DATA_FILE_NAME = "Environmental_Sensing.json"

def json_record(dstamp, tstamp, pressure, temp_f, temp_c, humidity):
    return '{ ' + '"date": {0:8s}, "time": {1:6s}, "pressure": {2:8.2f}, "temp_f": {3:4.1f}, "temp_c": {4:4.1f}, "humidity": {5:4.1f}'.format(dstamp, tstamp, pressure, temp_f, temp_c, humidity) + ' }'

#    Conversion functions
def celsius_to_fahrenheit(celsius):   
    return (celsius * 1.8) + 32

def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) / 1.8

#    Create a SenseHat instance
sense = SenseHat()
sense.clear(BLACK)
sleep(2.0)

#    Initialize the loop
count = 0

while True:
    count += 1

    print("Loop: {0:6d}".format(count))
    acceleration = sense.get_accelerometer_raw()

    xA = acceleration["x"]
    xAr = round(xA)

    yA = acceleration["y"]
    yAr = round(yA)

    zA = acceleration["z"]
    zAr = round(zA)
    
    print("{0:12d}: xA = {1:10.7f}, xAr = {2:2.1f}, yA = {3:10.7f}, yAr = {4:2.1f}, zA = {5:10.7f}, zAr = {6:2.1f}". format(count, xA, xAr, yA, yAr, zA, zAr))
    
    orientation = sense.get_gyroscope_raw()

    xO = orientation["x"]
    xOr = round(xO)

    yO = orientation["y"]
    yOr = round(yO)

    zO = orientation["z"]
    zOr = round(zO)
    
    print("{0:12d}: xO = {1:10.7f}, xOr = {2:2.1f}, yO = {3:10.7f}, yOr = {4:2.1f}, zO = {5:10.7f}, zOr = {6:2.1f}". format(count, xO, xOr, yO, yOr, zO, zOr))
    print()
    
    north = sense.get_compass()
    print("North = {0}".format(north))
    print()

    sleep(DEFAULT_DELAY_SEC)

    