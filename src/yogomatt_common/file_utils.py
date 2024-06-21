import os
import time

def init_csv_file():
    try:
      file_dir = '/home/byron/logs'
      file_exists = os.path.exists(file_dir)
      if not file_exists:
        os.makedirs(file_dir)

      file_path = '{0}/{1}.csv'.format(file_dir, time.strftime('%y-%m-%d'))
      f = open(file_path, 'a+')
      if os.stat(file_path).st_size == 0:
        f.write('Timestamp,Measure_Type,Measure_Unit,Measure_Value\r\n')
      
      return f
    except Exception as error:
      print(error.args[0])
      raise error

def write_to_file(file, sample_time, measure_type, measure_unit, measure_value):
   file.write('{0},{1},{2},{3:0.1f}\r\n'.format(sample_time,
                measure_type, measure_unit, measure_value))