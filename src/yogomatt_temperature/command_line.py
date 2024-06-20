import yaml
import logging.config
from yogomatt_temperature.dht22reader import *
from yogomatt_temperature.ds18b20reader import *

#CONFIG_DIR = "../config"
#LOG_DIR = "../logs"

LOGGING_FILE = "logging.yaml"

def setup_logging():
  #logging_config_path = '/'.join([CONFIG_DIR, LOGGING_FILE])
  
  with open(LOGGING_FILE) as f:
    config_dict = yaml.load(f, Loader=yaml.Loader)

  logging.config.dictConfig(config_dict)
  log = logging.getLogger('sensor')
  log.info('Logging init done')

setup_logging()

def dht22():
  read_dht22()

def ds18b20():
  read_ds18b20()
