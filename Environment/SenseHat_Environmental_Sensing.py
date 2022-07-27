#!/usr/bin/env python3
from sense_hat import SenseHat
from time import sleep
from os import path
from datetime import datetime
import json

#    Feature controls
USING_TEXT_CONSOLE = True
USING_SENSE_RGB_MATRIX = False
USING_DATA_LOGGING = True
USING_DATA_LOGGING_CONSOLE = False

#    Set up colors
RED			      =	(255, 0, 0)
GREEN		      =	(0, 255, 0)
BLUE		      =	(0, 0, 255)
COBALT_BLUE   = (0, 0, 125)

ALL_BLACK	    =	(0, 0, 0)
ALL_WHITE	    =	(255, 255, 255)

CYAN		      =	(0, 255, 255)
MAGENTA       =	(255, 0, 255)
ORANGE        = (125, 125, 0)
YELLOW        =	(255, 255, 0)
MEDIUM_YELLOW =	(125, 125, 0)
DARK_YELLOW   =	(50, 50, 0)

#    Default settings
MINUTE_SECONDS = 60

DEFAULT_BACKGROUND_COLOR = COBALT_BLUE
DEFAULT_TEXT_COLOR = YELLOW

DEFAULT_SCROLL_SPEED = 0.045
DEFAULT_DELAY_SEC = 2.60
DEFAULT_READING_INTERVAL_MIN = 10.0
DEFAULT_NUM_CYCLES = 1

MAX_LOOPS = 10
DATA_FILE_NAME = "/home/hybotics/Projects/Python/Python/SenseHat/Data/SenseHat_Environmental_Sensing.json"

def new_json_record(dstamp, tstamp, pressure, temp_f, temp_c, humidity):
    return '{ ' + '"date": "{0:8s}", "time": "{1:6s}", "pressure": {2:6.1f}, "temp_f": {3:4.1f}, "temp_c": {4:4.1f}, "humidity": {5:4.1f}'.format(dstamp, tstamp, pressure, temp_f, temp_c, humidity) + ' }'

#    Conversion functions
def to_fahrenheit(celsius):
    return (celsius * 1.8) + 32

def to_celsius(fahrenheit):
    return (fahrenheit - 32) / 1.8

def show(msg, cycles=1, msg_delay_sec=DEFAULT_DELAY_SEC, scr_speed=DEFAULT_SCROLL_SPEED, txt_color=DEFAULT_TEXT_COLOR, bg_color=DEFAULT_BACKGROUND_COLOR):
    for cyc in range(cycles):
        sense.show_message(msg, back_colour=bg_color, text_colour=txt_color, scroll_speed=scr_speed)
        sleep(msg_delay_sec)

#    Create a SenseHat instance
sense = SenseHat()
sense.clear(ALL_BLACK)
sleep(1.0)

#    Initialize the loop
count = 0
json_data = ""
json_output = ""

try:
    while True:
        count += 1

        # Get data from the sensors
        pressure = sense.get_pressure()

        temperature_celsius = sense.get_temperature()
        temperature_fahrenheit = to_fahrenheit(temperature_celsius)

        temperature_celsius_from_pressure = sense.get_temperature_from_pressure()
        temperature_fahrenheit_from_pressure = to_fahrenheit(temperature_celsius_from_pressure)

        real_temperature_celsius = (temperature_celsius_from_pressure + temperature_celsius) / 2
        real_temperature_fahrenheit = to_fahrenheit(real_temperature_celsius)

        humidity = sense.get_humidity()

        if USING_DATA_LOGGING:
            #    Get updated date and time from an RTC or system time here (TBD)
            new_date = datetime.today()
            new_time = datetime.now()
            new_ds = new_date.strftime("%Y%m%d")
            new_ts = new_time.strftime("%H%M%S")

            #    Set the open mode for the data file
            if path.exists(DATA_FILE_NAME):
                open_mode = "a"
            else:
                open_mode = "w"

            if USING_TEXT_CONSOLE or USING_DATA_LOGGING_CONSOLE:
                print()

            if USING_DATA_LOGGING_CONSOLE:
                # Format the readings data into JSON
                json_data = new_json_record(new_ds, new_ts, pressure, real_temperature_fahrenheit, real_temperature_celsius, humidity)

                # Write the readings to the data file
                with open(DATA_FILE_NAME, open_mode) as jf:
                  # json.dump(json_data, jf, indent=2)
                  jf.write(json_data + "\n")

                #json_output = json.dumps(json_data)

                print("JSON data = '{0}'".format(json_data))
                #print("JSON Out = '{0}'".format(json_output))


        if USING_TEXT_CONSOLE:
            print()
            print("***** Reading {0:5d} ({1} minute intervals)".format(count, DEFAULT_READING_INTERVAL_MIN))
            print("Pressure is {0:6.1f} millibars".format(pressure))
            print()
            print("Temperature is {0:4.1f}°F ({1:4.1f}°C)".format(temperature_fahrenheit, temperature_celsius))
            print("Temperature from Pressure is {0:4.1f}°F ({1:4.1f}°C)".format(temperature_fahrenheit_from_pressure, temperature_celsius_from_pressure))
            print("Real Temperature is {0:4.1f}°F ({1:4.1f}°C)".format(real_temperature_fahrenheit, real_temperature_celsius))
            print()
            print("Humidity is {0:4.1f}%".format(humidity))
            print()

        if USING_SENSE_RGB_MATRIX:
            #    If enabled, display the readings on the Sense HAT RGB Matrix
            message = "Reading {0} ({1:3.1f} minute intervals)".format(count, DEFAULT_READING_INTERVAL_MIN)
            show(message, DEFAULT_NUM_CYCLES, DEFAULT_DELAY_SEC, 0.035, ORANGE)

            message = "Pressure: {0:6.1f} millibars".format(pressure)
            show(message, DEFAULT_NUM_CYCLES, DEFAULT_DELAY_SEC, DEFAULT_SCROLL_SPEED, GREEN)

            message = "Temperature: {0:4.1f}F ({1:4.1f}C)".format(real_temperature_fahrenheit, real_temperature_celsius)
            show(message, DEFAULT_NUM_CYCLES, DEFAULT_DELAY_SEC, 0.065, YELLOW)

            message = "Humidity: {0:4.1f}%".format(humidity)
            show(message, DEFAULT_NUM_CYCLES, DEFAULT_DELAY_SEC, 0.065, CYAN)

            message = "Temperature: {0:4.1f}F ({1:4.1f}C)".format(real_temperature_fahrenheit, real_temperature_celsius)
            show(message, DEFAULT_NUM_CYCLES, DEFAULT_DELAY_SEC, 0.065, YELLOW)

            message = "Humidity: {0:4.1f}%".format(humidity)
            show(message, DEFAULT_NUM_CYCLES, DEFAULT_DELAY_SEC, 0.065, CYAN)

            sense.clear(ALL_BLACK)

        # Sleep until it is time for the next reading
        if USING_TEXT_CONSOLE:
            print("Sleeping for {0} (minutes) * {1} (seconds/minute) = {2} seconds".format(DEFAULT_READING_INTERVAL_MIN, MINUTE_SECONDS, DEFAULT_READING_INTERVAL_MIN * MINUTE_SECONDS))

        sleep(DEFAULT_READING_INTERVAL_MIN * MINUTE_SECONDS)

except KeyboardInterrupt:
    sense.clear(ALL_BLACK)
    print("Exiting by Ctrl/C")
    print()
