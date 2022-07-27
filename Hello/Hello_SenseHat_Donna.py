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

#    Default settings
DEFAULT_SCROLL_SPEED = 0.075
DELAY_SEC = 1.30
MAX_LOOPS = 2

#    Create a SenseHat instance
sense = SenseHat()

#    Initialize the loop
looper = 0

#    Main Loop
while looper < MAX_LOOPS:
	sense.show_message("Hello, Donna!", text_colour=COBALT_BLUE, back_colour=BLACK, scroll_speed=DEFAULT_SCROLL_SPEED)
	sleep(DELAY_SEC)

	sense.show_message("How are you today?", text_colour=COBALT_BLUE, back_colour=BLACK, scroll_speed=DEFAULT_SCROLL_SPEED)
	sleep(DELAY_SEC * 2)
	
	looper += 1

#    Clean up and exit
sense.clear()
