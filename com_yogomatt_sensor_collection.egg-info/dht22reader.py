import os
import time
import board
import adafruit_dht
import requests

# Constants
TEMPERATURE_REST_API_URL = 'http://192.168.0.160:8080/api/measure'
HUMIDITY_REST_API_URL = 'http://192.168.0.160:8080/api/measure'

# Initiate the dht device, with data pin connected to:
dhtDevice = adafruit_dht.DHT22(board.D22, use_pulseio=False)

# you can pass DHT22 use_pulseio=False if you wouldn't like to use pulseio.
# This may be necessary on a Linux single board computer like the Raspberry Pi,
# but it will not work in CircuitPython.
# dhtDevice = adafruit_dht.DHT22(board.D18, use_pulseio=False)

# Init the cvs file
try:
    file_path = '/home/byron/my_logs/{0}.csv'.format(time.strftime('%y-%m-%d'))
    f = open(file_path, 'a+')
    if os.stat(file_path).st_size == 0:
        f.write('Date,Time,Temperature,Humidity\r\n')
except Exception as error:
    print(error.args[0])
    raise error

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
            f.write('{0} {1:0.1f} C {2:0.1f}\r\n'.format(sample_time,
                temperature_c, humidity))
        else:
            print('Failed to retrieve the sensor data')

        # Store in the "cloud"
        # headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        headers = {'Content-Type': 'application/json'}

        sampleTemperature = {
            "sampleDate": sample_time,
            "sampleType": "temperature",
            "deviceId": "DHT22",
  	    "measure": {
		"type": "centigrades",
            	"value": str(temperature_c)
	    }
        }

        resp = requests.post(TEMPERATURE_REST_API_URL, json = sampleTemperature, headers = headers)

        print(resp)

        sampleHumidity = {
            "sampleDate": sample_time,
            "sampleType": "humidity",
            "deviceId": "DHT22",
            "measure": {
		"type": "percentage",
           	"value": str(humidity)
            }
        }

        resp = requests.post(HUMIDITY_REST_API_URL, json = sampleHumidity, headers = headers)

        print(resp)
    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error

    time.sleep(300.0)
