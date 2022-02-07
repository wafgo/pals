#!/usr/bin/python3

import requests
import os
import time

try:    
    default_ip = os.environ['PALS_GW_IP']
except KeyError:
    default_ip = '192.168.0.141'

try:    
    default_deconz_app_id = os.environ['PALS_DECONZ_API_ID']
except KeyError:
    default_deconz_app_id = ''

url = "http://" + default_ip + "/api/" + default_deconz_app_id +"/groups/2"
is_on = requests.get(url).json()['state']['all_on']
retry_count = 1

while not is_on and retry_count < 100:
    print("Try # " + str(retry_count) + " to enable " + url + '/action ')
    on_data = '{"on": true}'
    r = requests.put(url + '/action', data=on_data)
    time.sleep(5)
    r = requests.get(url)
    is_on = r.json()['state']['all_on']
    retry_count += 1
    
