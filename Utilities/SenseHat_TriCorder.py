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

DEFAULT_TEXT_COLOR = MAGENTA
DEFAULT_SCROLL_SPEED = 0.085
DEFAULT_DELAY_SEC = 2.60
DEFAULT_READING_INTERVAL_MIN = 5.0

#    Conversion functions
def to_fahrenheit(celsius):
    return (celsius * 1.8) + 32

def to_celsius(fahrenheit):
    return (fahrenheit - 32) / 1.8

#    Display a message on the Sense HAT RGB arraay
def show(msg, cycles=1, msg_delay_sec=DEFAULT_DELAY_SEC, bg_color=DEFAULT_BACKGROUND_COLOR, txt_color=DEFAULT_TEXT_COLOR, scr_speed=DEFAULT_SCROLL_SPEED):
    for cyc in range(cycles):
        sense.show_message(msg, back_colour=bg_color, text_colour=txt_color, scroll_speed=scr_speed)
        sleep(msg_delay_sec)
        sense.clear()

#    Get and display readings from the IMU
def orientation():
    orientation = sense.get_orientation()
    pitchR = round(orientation["pitch"], 1)
    rollR = round(orientation["roll"], 1)
    yawR = round(orientation["yaw"], 1)

    message = "Pitch: {0}, Roll: {1}, Yaw: {2}".format(pitchR, rollR, yawR)
    show(message)

#
#    Get and display readings from the Pressure, Temperature, Humidity sensors and Compass
#
#    Pressure sensor
def pressure():
    pressure = round(sense.get_pressure(), 1)

    message = "Pressure: {0:6.2f} millibars".format(pressure)
    show(message)

#    Temperature sensor
def temperature():
    celsius = round(sense.get_temperature(), 1)
    fahrenheit = round(to_fahrenheit(celsius), 1)
    
    message = "Temperature: {0:4.1f}F ({1:4.1f}C)".format(fahrenheit, celsius)
    show(message)

#    Humidity sensor
def humidity():
    humidity = round(sense.get_humidity(), 1)   

    message = "Humidity: {0:4.1f}%".format(humidity)
    show(message)

#    Compass
def compass():
    for i in range(25):
        north = sense.get_compass()
        
    north = round(north, 1)
    
    message = "North: {0} degrees".format(north)
    show(message)
    
#    Create a SenseHat instance
sense = SenseHat()
sense.clear(BLACK)
sleep(2.0)

#    Attach sensors to joystick directions
sense.stick.direction_up = orientation
sense.stick.direction_right = temperature
sense.stick.direction_down = compass
sense.stick.direction_left = pressure
sense.stick.direction_middle = humidity

#    Loop forever waiting for the joystick to be moved
while True:
    pass
