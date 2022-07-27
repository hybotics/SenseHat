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

MINUTE_SECONDS = 60
MAX_LOOPS = 10

#    Default settings
DEFAULT_BACKGROUND_COLOR = COBALT_BLUE
DEFAULT_TEXT_COLOR = YELLOW
DEFAULT_SCROLL_SPEED = 0.085
DEFAULT_DELAY_SEC = 2.60
DEFAULT_READING_INTERVAL_MIN = 5.0

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
looper = 0

while True:
    looper += 1

    orientation = sense.get_orientation()
    pitch = orientation["pitch"]
    roll = orientation["roll"]
    yaw = orientation["yaw"]

    print("Reading {0:6d}, Orientation = '{1}'".format(looper, orientation))
    print("                Pitch = {0:7.2f}, Roll = {1:7.2f}, Yaw = {2:7.2f}".format(pitch, roll, yaw))
    print()
    sleep(DEFAULT_DELAY_SEC)
