import os
import time
import board
import adafruit_dht
import file_utils
import api_utils

# DHT22 Module
def read_dht22():

  # Initiate the dht device, with data pin connected to:
  dhtDevice = adafruit_dht.DHT22(board.D22, use_pulseio=False)

  # you can pass DHT22 use_pulseio=False if you wouldn't like to use pulseio.
  # This may be necessary on a Linux single board computer like the Raspberry Pi,
  # but it will not work in CircuitPython.
  # dhtDevice = adafruit_dht.DHT22(board.D18, use_pulseio=False)

  # Init the cvs file
  csv_file = file_utils.init_csv_file()

  while True:
      try:
          # Print the values to the serial port
          sample_time = time.strftime('%Y-%m-%dT%H:%M:%S')
          temperature_c = dhtDevice.temperature
          temperature_f = temperature_c * (9 / 5) + 32
          humidity = dhtDevice.humidity
          print(
              "Time: {}  Temp: {:.1f} F / {:.1f} C  Humidity: {}% ".format(
                sample_time, temperature_f, temperature_c, humidity
              )
          )

          # Store in a cvs file
          if temperature_c is not None and humidity is not None:
              file_utils.write_to_file(csv_file, sample_time, 'temperature', 'centigrades', temperature_c)
              file_utils.write_to_file(csv_file, sample_time, 'temperature', 'percentage', humidity)
          else:
              print('Failed to retrieve data from sensor DHT22')

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
          print(error.args[0])
          time.sleep(2.0)
          continue
      except Exception as error:
          dhtDevice.exit()
          raise error

      time.sleep(300.0)
