from yogomatt_common.logging_config import *
from yogomatt_common.state_handler import *
from yogomatt_temperature.dht22reader import *
from yogomatt_temperature.ds18b20reader import *
from yogomatt_proximity.hcsr501pir_reader import *

setup_logging()

def dht22():
  try:
    read_dht22(turn_on_temperature_state, turn_off_temperature_state)
  except KeyboardInterrupt:
    turn_off_temperature_state()
    print('Program interrupted')
    pass

def ds18b20():
  try:
    read_ds18b20(turn_on_temperature_state, turn_off_temperature_state)
  except KeyboardInterrupt:
    turn_off_temperature_state()
    print('Program interrupted')
    pass

def hcsr501pir():
  try:
    read_hcsr501pir(turn_on_proximity_state, turn_off_proximity_state)
  except KeyboardInterrupt:
    turn_off_proximity_state()
    print('Program interrupted')
    pass
