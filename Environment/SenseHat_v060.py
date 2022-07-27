#!/usr/bin/env python3
'''
  Name:     SenseHat Environmental Sensing
  Author:   Dale Weber <hybotics.wy@gmail.com>

  Modification history:
  
  Purpose:  To get sensor readings from the Pimoroni SenseHat, display them, and log them to a JSON file
  Version:  0.5.0
  Date:     07-May-2022

  Purpose:  To add a configuration file to the script so I do not have to edit the script and then log in as
              root to restart the service. The script will watch for a change in the file and reread settings
              if there were change(s).
  Version:  0.6.0
  Date:     15-Jul-2022
'''
from multiprocessing.sharedctypes import Value
from sense_hat import SenseHat
from time import sleep
from os import path
from datetime import datetime
import json

# Debugging control
DEBUGGING = True

# Feature controls
USING_DATA_CONSOLE = False
USING_TEXT_CONSOLE = True

USING_SENSE_RGB_MATRIX = False
USING_DATA_LOGGING = False

DEFAULT_SCROLL_SPEED = 0.045
DEFAULT_DELAY_SEC = 2.60
DEFAULT_READING_INTERVAL_MIN = 5.0
DEFAULT_NUM_CYCLES = 1

MAX_LOOPS = 10

# Set up colors
RED			      =	(255, 0, 0)
GREEN		      =	(0, 255, 0)
BLUE		      =	(0, 0, 255)
COBALT_BLUE   = (0, 0, 125)

BLACK	        =	(0, 0, 0)
WHITE	        =	(255, 255, 255)

CYAN		      =	(0, 255, 255)
MAGENTA       =	(255, 0, 255)
ORANGE        = (125, 125, 0)
YELLOW        =	(255, 255, 0)
MEDIUM_YELLOW =	(125, 125, 0)
DARK_YELLOW   =	(50, 50, 0)

# Default settings
MINUTE_SECONDS = 60

DEFAULT_BACKGROUND_COLOR = COBALT_BLUE
DEFAULT_TEXT_COLOR = YELLOW

DEFAULT_SCROLL_SPEED = 0.045
DEFAULT_DELAY_SEC = 2.60
DEFAULT_READING_INTERVAL_MIN = 5.0
DEFAULT_NUM_CYCLES = 1

MAX_LOOPS = 10

JSON_FILE_NAME = "/home/hybotics/Projects/Python/Python/SenseHat/Data/SenseHat.json"
CONFIG_FILE_NAME = "/home/hybotics/Projects/Python/Python/SenseHat/SenseHat.config"

SETTINGS_LABELS = [ "data_console", "text_console", "interval", "use_matrix", "data_logging", "debugging" ]
SETTINGS_TYPES = ["B", "B", "F", "B", "B", "B" ]

def new_json_record(dstamp, tstamp, pressure, temp_f, temp_c, temp_c_pressure, humidity):
  return '{ ' + '"date": "{0:8s}", "time": "{1:6s}", "pressure": {2:6.1f}, "temp_f": {3:4.1f}, "temp_c": {4:4.1f}, "temp_c_fp": {4:4.1f}, "humidity": {5:4.1f}'.format(dstamp, tstamp, pressure, temp_f, temp_c, temp_c_pressure, humidity) + ' }'

# Conversion functions
def to_fahrenheit(celsius):
  return (celsius * 1.8) + 32

def to_celsius(fahrenheit):
  return (fahrenheit - 32) / 1.8

def show(msg, cycles=1, msg_delay_sec=DEFAULT_DELAY_SEC, scr_speed=DEFAULT_SCROLL_SPEED, txt_color=DEFAULT_TEXT_COLOR, bg_color=DEFAULT_BACKGROUND_COLOR):
  for cyc in range(cycles):
    sense.show_message(msg, back_colour=bg_color, text_colour=txt_color, scroll_speed=scr_speed)
    sleep(msg_delay_sec)

def find_setting(setting, settings_list):
  result = 0
  slen = len(settings_list)
  nr = 0

  for n in range(slen):
    print(f"{n + 1} : {settings_list[n]}")

  while nr < slen and setting != settings_list[nr][0]:
    nr += 1

  if nr >= slen:
    result = None
  else:
    result = settings_list[nr][1]

  return result

def get_settings(cf_name, s_labels, s_types):
  '''
    Get settings from the configuration file
  '''
  with open(cf_name, "r") as cf:
    # Read settings from an existing configuration file
    lcount = 0
    line = cf.readline()
    settings_list = []

    #
    # Process the configuration file
    #
    while line:
      line = line.strip()
      lcount += 1

      try:
        setting, value = line.split("=")
      except ValueError:
        emsg = f"Separator '=' not found at line {lcount} in configuration file {cf_name}!"
        raise ValueError(emsg)

      value = value.upper()
      setting = setting.lower()

      if setting in s_labels:
        setting_lindex = s_labels.index(setting)
        setting_type = s_types[setting_lindex]
      else:
        emsg = f"The setting '{setting}' is not valid at line {lcount} in configuration file {cf_name}!"
        raise ValueError(emsg)

      #
      # Process the setting by type
      #
      u_value = value.upper()
      u_type = setting_type.upper()

      if u_type == "B":
      # Boolean
        if u_value == "TRUE":
          value = True
        elif u_value == 'FALSE':
          value = False
        else:
          emsg = f"Invalid value ('{value}') for setting '{setting}' in configuration file {cf_name} at line {lcount}' - Must be 'True' or 'False'"
          raise ValueError(emsg)
      elif u_type == "F":
      # Floating Point
        try:
          value = float(u_value)
        except ValueError:
          emsg = f"Invalid floating point value ({u_value}) for setting '{setting}' in configuration file {cf_name} at line {lcount}!"
          raise ValueError(emsg)
      elif u_type == "I":
        # Integer
        try:
          value = int(u_value)
        except ValueError:
          emsg = f"Invalid integer value ({u_value}) for setting '{setting}' in configuration file {cf_name} at line {lcount}!"
          raise ValueError(emsg)
      elif u_type == "S":
        # String
        emdg = f"Strings are not supported at this time for setting '{setting}' in confioguration file {cf_name} at line {lcount}!"
        raise ValueError(emsg)
      else:
        emsg = f"Invalid setting type ('{setting_type}') in configuration file {cf_name} at line {lcount}!"
        raise ValueError(emsg)

      settings_list.append([setting, value])

      line = cf.readline()

  return settings_list

def init_settings(cf_name, s_labels, s_types):
  '''
    Initialize the settings in the script
  '''
  s_list = get_settings(cf_name, s_labels, s_types)

  DEBUGGING = find_setting("debugging", s_list)
  USING_DATA_CONSOLE = find_setting("data_console", s_list)
  USING_TEXT_CONSOLE = find_setting("text_console", s_list)
  DEFAULT_READING_INTERVAL_MIN = find_setting("interval", s_list)
  USING_SENSE_RGB_MATRIX = find_setting("use_matrix", s_list)
  USING_DATA_LOGGING = find_setting("data_logging", s_list)

# Initialize the settings from the config file or initialize a new configuration file
def put_settings(cf_name=CONFIG_FILE_NAME, s_labels=SETTINGS_LABELS, s_types=SETTINGS_TYPES):
  '''
    Initialize a brand new condifuration file
  '''
  with open(cf_name, "w") as cf:
    line = f"data_console={USING_DATA_CONSOLE}\n"
    settings_list.append(["data_console", USING_DATA_CONSOLE])
    cf.write(line)

    line = f"text_console={USING_TEXT_CONSOLE}\n"
    settings_list.append(["text_console", USING_TEXT_CONSOLE])
    cf.write(line)

    line = f"use_matrix={USING_SENSE_RGB_MATRIX}\n"
    settings_list.append(["use_matrix", USING_SENSE_RGB_MATRIX])
    cf.write(line)

    line = f"data_logging={USING_DATA_LOGGING}\n"
    settings_list.append(["data_logging", USING_DATA_LOGGING])
    cf.write(line)

    line = f"interval={DEFAULT_READING_INTERVAL_MIN}\n"
    settings_list.append(["interval", DEFAULT_READING_INTERVAL_MIN])
    cf.write(line)

    line = f"debugging={DEBUGGING}\n"
    settings_list.append(["data_logging", DEBUGGING])
    cf.write(line)

  return settings_list

'''
  Script initialization
'''

#	Create a SenseHat instance
sense = SenseHat()
sense.clear(BLACK)
sense.set_rotation(180)
sleep(1.0)

# Get settings from the configuration file
settings_list = init_settings(CONFIG_FILE_NAME, SETTINGS_LABELS, SETTINGS_TYPES)

if DEBUGGING:
  slen = len(settings_list)

  for setting_nr in range(slen):
    print(f"Setting: {settings_list[setting_nr][0]}, Value = {settings_list[setting_nr][1]}")

#    Initialize the loop
count = 0
json_data = ""
json_output = ""
pressure = sense.get_pressure()

'''
  Main loop starts here
'''
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
      if path.exists(JSON_FILE_NAME):
        if USING_DATA_CONSOLE:
          print(f"Data file '{JSON_FILE_NAME}' exists")

        open_mode = "a"
      else:
        if USING_DATA_CONSOLE:
          print(f"Data file '{JSON_FILE_NAME}' does not exist")

        open_mode = "w"

      if USING_DATA_CONSOLE:
        print(f"Data file '{JSON_FILE_NAME}', Open mode: '{open_mode}'")

      if USING_TEXT_CONSOLE or USING_DATA_CONSOLE:
        print()

      # Format the readings data into JSON
      json_data = new_json_record(new_ds, new_ts, pressure, temperature_fahrenheit, temperature_celsius, temperature_celsius_from_pressure, humidity)

      if USING_DATA_CONSOLE:
        print(f"JSON data = '{json_data}'")

      # Write the readings to the data file
      with open(JSON_FILE_NAME, open_mode) as jf:
        if USING_DATA_CONSOLE:
          print(f"Writing data to {JSON_FILE_NAME}")
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

      sense.clear(BLACK)

    # Sleep until it is time for the next reading
    if USING_TEXT_CONSOLE:
      print("Sleeping for {0} (minutes) * {1} (seconds/minute) = {2} seconds".format(DEFAULT_READING_INTERVAL_MIN, MINUTE_SECONDS, DEFAULT_READING_INTERVAL_MIN * MINUTE_SECONDS))

    sleep(DEFAULT_READING_INTERVAL_MIN * MINUTE_SECONDS)
except KeyboardInterrupt:
  sense.clear(BLACK)
  print("Exiting by Ctrl/C")
  print()
