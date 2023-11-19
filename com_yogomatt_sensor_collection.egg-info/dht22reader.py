import os
import time
import board
import adafruit_dht
import requests

# Constants
TEMPERATURE_REST_API_URL = 'http://192.168.0.102:8081/temperature'
HUMIDITY_REST_API_URL = 'http://192.168.0.102:8081/humidity'

# Initiate the dht device, with data pin connected to:
dhtDevice = adafruit_dht.DHT22(board.D22, use_pulseio=False)

# you can pass DHT22 use_pulseio=False if you wouldn't like to use pulseio.
# This may be necessary on a Linux single board computer like the Raspberry Pi,
# but it will not work in CircuitPython.
# dhtDevice = adafruit_dht.DHT22(board.D18, use_pulseio=False)

# Init the cvs file
try:
    file_path = './logs/{0}.csv'.format(time.strftime('%y-%m-%d'))
    f = open(file_path, 'a+')
    if os.stat(file_path).st_size == 0:
        f.write('Date,Time,Temperature,Humidity\r\n')
except Exception as error:
    print(error.args[0])
    raise error

while True:
    try:
        # Print the values to the serial port
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
        print(
            "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
                temperature_f, temperature_c, humidity
            )
        )

        # Store in a cvs file
        if temperature_c is not None and humidity is not None:
            f.write('{0} {1} {2:0.1f} C {3:0.1f}\r\n'.format(time.strftime('%Y/%m/%d'),
                time.strftime('%H:%M:%S'), temperature_c, humidity))
        else:
            print('Failed to retrieve the sensor data')

        # Store in the "cloud"
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        sampleTemperature = {
            "sampleDate": time.strftime('%Y-%m-%d'),
            "sampleTime": time.strftime('%H:%M:%S'),
            "device": "DHT22",
            "valueCentigrades": str(temperature_c)
        }

        resp = requests.post(TEMPERATURE_REST_API_URL, data = sampleTemperature, headers = headers)

        print(resp)

        sampleHumidity = {
            "sampleDate": time.strftime('%Y-%m-%d'),
            "sampleTime": time.strftime('%H:%M:%S'),
            "device": "DHT22",
            "value": str(humidity)
        }

        resp = requests.post(HUMIDITY_REST_API_URL, data = sampleHumidity, headers = headers)

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
