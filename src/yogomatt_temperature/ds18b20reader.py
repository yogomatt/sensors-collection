import os
import glob
import time
import yogomatt_temperature.file_utils as file_utils
import yogomatt_temperature.api_utils as api_utils

def init_device():
  os.system('modprobe w1-gpio')
  os.system('modprobe w1-therm')

  base_dir = '/sys/bus/w1/devices/'
  device_folder = glob.glob(base_dir + '28*')[0]
  device_file = device_folder + '/w1_slave'
  
  return device_file

def read_temp_raw(device_file):
  f = open(device_file, 'r')
  lines = f.readlines()
  f.close()
  return lines

def read_temp(device_file):
  lines = read_temp_raw(device_file)
  while lines[0].strip()[-3:] != 'YES':
    time.sleep(0.2)
    lines = read_temp_raw(device_file)
  equals_pos = lines[1].find('t=')
  if equals_pos != -1:
    temp_string = lines[1][equals_pos+2:]
    temp_c = float(temp_string) / 1000.0
    temp_c = round(temp_c, 1)
    temp_f = temp_c * 9.0 / 5.0 + 32.0
    temp_f = round(temp_f, 1)
    return temp_c, temp_f

def read_ds18b20():
  device_file = init_device()
  csv_file = file_utils.init_csv_file()

  while True:
    try:
      sample_time = time.strftime('%Y-%m-%dT%H:%M:%S')
      temp_celsius, temp_fahrenheit = read_temp(device_file)

      print('Temperature: {0:.2f} C, {1:.2f} F'.format(temp_celsius, temp_fahrenheit))
      
      # Store in a cvs file
      if temp_celsius is not None:
          file_utils.write_to_file(csv_file, sample_time, 'temperature', 'centigrades', temp_celsius)
      else:
          print('Failed to retrieve data from sensor ds18b20')

      sample_temperature = {
        "sampleDate": sample_time,
        "sampleType": "temperature",
        "deviceId": "DS18B20",
        "measure": {
          "type": "centigrades",
          "value": str(temp_celsius)
        }
      }

      api_utils.post_sample(sample_temperature)
    except Exception as error:
      raise error
    
    time.sleep(300)
