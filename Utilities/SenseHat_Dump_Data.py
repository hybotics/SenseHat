#!/usr/bin/env python3
from sense_hat import SenseHat
from time import sleep
from os import path
import json

#    Feature controls
USING_TEXT_CONSOLE = True
USING_SENSE_RGB_MATRIX = True
USING_DATA_LOGGING = True

#    Set up colors
RED			  =	(255, 0, 0)
GREEN		  =	(0, 255, 0)
BLUE		  =	(0, 0, 255)
COBALT_BLUE   = (0, 0, 125)

ALL_BLACK	  =	(0, 0, 0)
ALL_WHITE	  =	(255, 255, 255)

CYAN		  =	(0, 255, 255)
MAGENTA       =	(255, 0, 255)
ORANGE        = (75, 75, 0)
YELLOW        =	(255, 255, 0)
MEDIUM_YELLOW =	(125, 125, 0)
DARK_YELLOW   =	(50, 50, 0)

#    Default settings
MINUTE_SECONDS = 60

DEFAULT_BACKGROUND_COLOR = COBALT_BLUE
DEFAULT_TEXT_COLOR = YELLOW

DEFAULT_SCROLL_SPEED = 0.045
DEFAULT_DELAY_SEC = 2.60
DEFAULT_READING_INTERVAL_MIN = 5.0
DEFAULT_NUM_CYCLES = 1

MAX_LOOPS = 10
DATA_FILE_NAME = "Data/Environmental_Sensing.json"

#    Initialize the loop
count = 0
inp = " "

jf = open(DATA_FILE_NAME, "r")

try:
    while(inp > ""):
        count += 1

        inp = json.load(jf)

        if USING_TEXT_CONSOLE:
            print("count = {0:5d}, inp = '{1}".format(count, inp))
except KeyboardInterrupt:
    jf.close()
    print("Exiting due to Ctrl/C")

jf.close()
