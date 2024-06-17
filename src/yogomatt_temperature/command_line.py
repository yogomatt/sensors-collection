import yaml
import logging.config
from yogomatt_temperature.dht22reader import *
from yogomatt_temperature.ds18b20reader import *

CONFIG_DIR = "./config"
LOG_DIR = "./logs"

LOGGING_FILE = "logging.yaml"

def __init__(self):
  setup_logging()

def setup_logging():
  logging_config_path = '/'.join(CONFIG_DIR, LOGGING_FILE)

  with open(logging_config_path) as f:
    config_dict = yaml.load(f)

  logging.config.dictConfig(config_dict)

def dht22():
  read_dht22()

def ds18b20():
  read_ds18b20()