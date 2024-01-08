import requests

BASE_URL = 'http://192.168.0.160:8080'
API_URL = BASE_URL + '/api/measure'

def post_sample(sample_json):
    # Store in the "cloud"
    # headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    headers = {'Content-Type': 'application/json'}
    resp = requests.post(API_URL, json = sample_json, headers = headers)

    print(resp)
