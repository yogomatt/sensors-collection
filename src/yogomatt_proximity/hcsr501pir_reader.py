
import RPi.GPIO as GPIO
import time
import logging
import yogomatt_common.api_utils as api_utils

log = logging.getLogger('sensor')

pir_gpio = 12

def read_hcsr501pir(turn_on_state, turn_off_state):

  log.info('Initiating device HC SR501 PIR')

  GPIO.setmode(GPIO.BCM)
  GPIO.setup(pir_gpio, GPIO.IN)

  try:
    while True:
      if GPIO.input(pir_gpio) == 1:
        turn_on_state()
        post_motion()
      elif GPIO.input(pir_gpio) == 0:
        turn_off_state()
    
      time.sleep(30)
  except KeyboardInterrupt:
    GPIO.cleanup()
    turn_off_state()
    raise

def post_motion():
  sample_time = time.strftime('%Y-%m-%dT%H:%M:%S')

  log.info(f"Motion detected at {sample_time}")

  # Build request
  sample_proximity = {
    "sampleDate": sample_time,
    "sampleType": "proximity",
    "deviceId": "HCSR501PIR",
    "measure": {
      "type": "signal",
      "value": "1"
    }
  }

  api_utils.post_sample(sample_proximity)
