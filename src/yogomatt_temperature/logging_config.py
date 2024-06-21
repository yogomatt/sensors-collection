import os
import logging

def setup_logging():
  # Create a console and file handlers
  console_handler = get_console_handler(get_simple_formatter())
  file_handler = get_file_handler('/tmp/sensor_collection', get_simple_formatter())

  # create the logger
  log = logging.getLogger('sensor')
  log.setLevel(logging.DEBUG)
  log.addHandler(console_handler)
  log.addHandler(file_handler)
  
  log.info('Logging init done')

def get_simple_formatter():
  # create formatter
  formatter = logging.Formatter('%(asctime)s - %(module)s - %(levelname)s: %(message)s')
  return formatter

def get_console_handler(formatter):
  ch = logging.StreamHandler()
  ch.setLevel(logging.DEBUG)
  ch.setFormatter(formatter)
  return ch

def get_file_handler(log_dir, formatter):
  log_file = os.path.join(log_dir, "log_app.log")
  fh = logging.handlers.RotatingFileHandler(filename=log_dir, maxBytes=1024 * 1024 * 5, backupCount=5)
  fh.setFormatter(formatter)
  return fh