import requests
import logging

BASE_URL = 'http://192.168.0.160:8080'
API_URL = BASE_URL + '/api/measure'

def __init__(self):
   self.log = logging.getLogger(__name__)

def post_sample(self, sample_json):
    # Store in the "cloud"
    self.log.info(f'Posting {sample_json}')

    # headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    headers = {'Content-Type': 'application/json'}
    resp = requests.post(API_URL, json = sample_json, headers = headers)

    self.log.info(f'Response received: {resp}')
