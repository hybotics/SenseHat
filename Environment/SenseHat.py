#!/usr/bin/env python3
from sense_hat import SenseHat
from time import sleep
from os import path
from datetime import datetime
import json

#    Feature controls
USING_DATA_CONSOLE = True
USING_TEXT_CONSOLE = True

USING_SENSE_RGB_MATRIX = True
USING_DATA_LOGGING = True

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
DEFAULT_READING_INTERVAL_MIN = 5.0
DEFAULT_NUM_CYCLES = 1

MAX_LOOPS = 10
JSON_FILE_NAME = "/home/hybotics/Projects/Python/Python/SenseHat/Data/SenseHat.json"

#out_file_name = path.realpath(JSON_FILE_NAME)
out_file_name = JSON_FILE_NAME

def new_json_record(dstamp, tstamp, pressure, temp_f, temp_c, temp_c_pressure, humidity):
  return '{ ' + '"date": "{0:8s}", "time": "{1:6s}", "pressure": {2:6.1f}, "temp_f": {3:4.1f}, "temp_c": {4:4.1f}, "temp_c_fp": {4:4.1f}, "humidity": {5:4.1f}'.format(dstamp, tstamp, pressure, temp_f, temp_c, temp_c_pressure, humidity) + ' }'

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
sense.set_rotation(180)
sleep(1.0)

#    Initialize the loop
count = 0
json_data = ""
json_output = ""
pressure = sense.get_pressure()

try:
  while True:
    count += 1

    # Get data from the sensors
    #
    # Get the pressure and make sure it is valid
    while pressure < 1.0:
      pressure = sense.get_pressure()
      sleep(0.5)

    temperature_celsius = sense.get_temperature()
    temperature_fahrenheit = to_fahrenheit(temperature_celsius)

    temperature_celsius_from_pressure = sense.get_temperature_from_pressure()
    temperature_fahrenheit_from_pressure = to_fahrenheit(temperature_celsius_from_pressure)

    real_temperature_celsius = (temperature_celsius_from_pressure + temperature_celsius) / 2
    real_temperature_fahrenheit = to_fahrenheit(real_temperature_celsius)

    humidity = sense.get_humidity()

    if USING_TEXT_CONSOLE or USING_DATA_CONSOLE:
      print()
      print(f"***** Reading {count:5d} ({DEFAULT_READING_INTERVAL_MIN} minute intervals)")
      print()

    if USING_DATA_LOGGING:
      #    Get updated date and time from an RTC or system time here (TBD)
      new_date = datetime.today()
      new_ds = new_date.strftime("%Y%m%d")

      new_time = datetime.now()
      new_ts = new_time.strftime("%H%M%S")

      #    Set the open mode for the data file
      if path.exists(out_file_name):
        if USING_DATA_CONSOLE:
          print(f"Data file '{out_file_name}' exists")

        open_mode = "a"
      else:
        if USING_DATA_CONSOLE:
          print(f"Data file '{out_file_name}' does not exist")

        open_mode = "w"

      if USING_DATA_CONSOLE:
        print(f"Data file '{out_file_name}', Open mode: '{open_mode}'")

      if USING_TEXT_CONSOLE or USING_DATA_CONSOLE:
        print()

      # Format the readings data into JSON
      json_data = new_json_record(new_ds, new_ts, pressure, temperature_fahrenheit, temperature_celsius, temperature_celsius_from_pressure, humidity)

      if USING_DATA_CONSOLE:
        print(f"JSON data = '{json_data}'")

      # Write the readings to the data file
      with open(out_file_name, open_mode) as jf:
        if USING_DATA_CONSOLE:
          print(f"Writing data to {out_file_name}")
          print()

        # json.dump(json_data, jf, indent=2)
        jf.write(json_data + "\n")

    if USING_TEXT_CONSOLE:
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
