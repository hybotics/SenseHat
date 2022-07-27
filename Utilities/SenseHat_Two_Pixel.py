#!/usr/bin/env python3
from sense_hat import SenseHat
from time import sleep

#    Set up colors
RED			 =	(255, 0, 0)
GREEN		 =	(0, 255, 0)
BLUE		 =	(0, 0, 255)
BLACK		 =	(0, 0, 0)
WHITE		 =	(255, 255, 255)

CYAN		 =	(0, 255, 255)
MAGENTA      =	(255, 0, 255)
ORANGE       =  (145, 75, 0)
YELLOW       =	(255, 255, 0)

#    Default settings
SCROLL_SPEED = 0.075
DELAY_SEC = 2.60
MAX_LOOPS = 5

#    Create a SenseHat instance
sense = SenseHat()
sense.clear()
sleep(1.0)

#    Initialize the loop
looper = 0

sense.set_pixel(0, 2, CYAN)
sense.set_pixel(7, 4, RED)
