import os
import time
import logging
import board
import adafruit_dht
#import yogomatt_temperature.file_utils as file_utils
import yogomatt_temperature.api_utils as api_utils

def __init__(self):
   self.log = logging.getLogger(__name__)

# DHT22 Module
def read_dht22(self):

  # Initiate the dht device, with data pin connected to:
  self.log.info('Initiating device DHT22 in pin 22')
  dhtDevice = adafruit_dht.DHT22(board.D22, use_pulseio=False)

  # you can pass DHT22 use_pulseio=False if you wouldn't like to use pulseio.
  # This may be necessary on a Linux single board computer like the Raspberry Pi,
  # but it will not work in CircuitPython.
  # dhtDevice = adafruit_dht.DHT22(board.D18, use_pulseio=False)

  # Init the cvs file
  # csv_file = file_utils.init_csv_file()

  while True:
      try:
          # Print the values to the serial port
          temperature_c = dhtDevice.temperature
          humidity = dhtDevice.humidity

          if temperature_c is None:
            self.log.error('Failed to retrieve temperature data from sensor DHT22')
            time.sleep(5)
            continue
          elif humidity is None:
            self.log.error('Failed to retrieve humidity data from sensor DHT22')
            time.sleep(5)
            continue
          
          sample_time = time.strftime('%Y-%m-%dT%H:%M:%S')
          temperature_f = temperature_c * (9 / 5) + 32

          self.log.info(
              "Time: {}  Temp: {:.1f} F / {:.1f} C  Humidity: {}% ".format(
                sample_time, temperature_f, temperature_c, humidity
              )
          )
        
          # Store in a cvs file
          # file_utils.write_to_file(csv_file, sample_time, 'temperature', 'centigrades', temperature_c)
          # file_utils.write_to_file(csv_file, sample_time, 'temperature', 'percentage', humidity)

          if temperature_c is not None:
            sample_temperature = {
                "sampleDate": sample_time,
                "sampleType": "temperature",
                "deviceId": "DHT22",
                "measure": {
                    "type": "centigrades",
                    "value": str(temperature_c)
                }
            }

            api_utils.post_sample(sample_temperature)

          if humidity is not None:
            sample_humidity = {
                "sampleDate": sample_time,
                "sampleType": "humidity",
                "deviceId": "DHT22",
                "measure": {
                    "type": "percentage",
                    "value": str(humidity)
                }
            }

            api_utils.post_sample(sample_humidity)

      except RuntimeError as error:
          # Errors happen fairly often, DHT's are hard to read, just keep going
          self.log.error(error.args[0])
          time.sleep(2.0)
          continue
      except Exception as error:
          dhtDevice.exit()
          self.log.error(error.args[0])
          raise error

      time.sleep(300.0)
