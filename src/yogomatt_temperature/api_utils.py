import requests
import logging

BASE_URL = 'http://192.168.0.160:8080'
API_URL = BASE_URL + '/api/measure'

log = logging.getLogger('sensor')

def post_sample(sample_json):
    # Store in the "cloud"
    log.info(f'Posting {sample_json}')

    # headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    headers = {'Content-Type': 'application/json'}
    resp = requests.post(API_URL, json = sample_json, headers = headers)

    log.info(f'Response received: {resp}')
