#!/usr/bin/env python3
from sense_hat import SenseHat
from time import sleep

RED		=	(255, 0, 0)
GREEN	=	(0, 255, 0)
BLUE	=	(0, 0, 255)
BLACK	=	(0, 0, 0)
WHITE	=	(255, 255, 255)

CYAN	=	(0, 255, 255)
MAGENTA	=	(255, 0, 255)
YELLOW	=	(255, 255, 0)

SCROLL_SPEED = 0.050
DELAY = 0.50
LOOPS = 5

sense = SenseHat()
looper = 0

while looper < LOOPS:
	sense.show_message("Hello World!", text_colour=YELLOW, back_colour=BLUE, scroll_speed=SCROLL_SPEED)
	sleep(DELAY)
	sense.clear()
	sleep(DELAY)
	
	looper += 1

sense.clear()
