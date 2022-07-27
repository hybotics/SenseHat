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
#    Create a SenseHat instance
sense = SenseHat()
sense.clear(ALL_BLACK)
sleep(2.0)

#    Initialize the loop
count = 0

jf = open(DATA_FILE_NAME, "r")
inp = jf.readline()

while(inp > ""):
    count += 1
    # inp = json.loads(jf)
    inp = inp.rstrip()
    print("{0:6d}: '{1}'".format(count, inp))
    #print("{inp) Date: '{0}', Time: '{1}".format(inp["date"], inp["time"]))

    js_data = json.loads(inp)
    print("{0:6d}: '{1}'".format(count, js_data))
    #print("(js_data) Date: '{0}', Time: '{1}".format(js_data["date"], js_data["time"]))
    print()

    inp = jf.readline()

