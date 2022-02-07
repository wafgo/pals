#!/usr/bin/python3
import requests
from datetime import datetime, timedelta
import argparse
import os

__version__major = '0'
__version__minor = '1'
__version__ = __version__major + '.' + __version__minor

try:
    default_app_id = os.environ['PALS_OWM_APP_ID']
except KeyError:
    default_app_id = ''

try:    
    default_ip = os.environ['PALS_GW_IP']
except KeyError:
    default_ip = '192.168.0.141'

try:    
    default_deconz_app_id = os.environ['PALS_DECONZ_API_ID']
except KeyError:
    default_deconz_app_id = ''

default_location_city = 'Mainhausen'
default_location_country_code = 'de'
        

parser = argparse.ArgumentParser(description='adjust cronjobs to start smart led lamps 30 minutes after sunset')
parser.add_argument('cronjob_file', metavar='cronjob_file', type=str, help='file to write to')
parser.add_argument('-a', '--app_id', default=default_app_id,
                    help='app id to use')
parser.add_argument('-t', '--town', default=default_location_city,
                    help='town of the sunset')
parser.add_argument('-i', '--ip_address', type=str, default=default_ip,
                    help='ip address of the gateway')
parser.add_argument('-d', '--deconz_app_id', type=str, default=default_deconz_app_id,
                    help='ip address of the gateway')
parser.add_argument('-c', '--country', default=default_location_country_code,
                    help='country of the town')

args = parser.parse_args()

if not args.app_id:
    print("Error: Please specify the Openweathermap app id either via --app_id/-a or via environment variable PALS_OWM_APP_ID")
    exit(1)

if not args.deconz_app_id:
    print("Error: Please specify the DECONZ api id either via --deconz_app_id/-d or via environment variable PALS_DECONZ_API_ID")
    exit(1)
    
response = requests.get('http://api.openweathermap.org/data/2.5/weather?q={},{}&APPID={}'.format(args.town, args.country, args.app_id)).json()

utc_sunset = response['sys']['sunset']
str_sunset = datetime.fromtimestamp(utc_sunset) + timedelta(minutes=30)

with open(args.cronjob_file, "w") as ctfile:
    ctfile.write(str(str_sunset.minute) + ' ' + str(str_sunset.hour) + ' * * * source /home/root/.bashrc; /usr/bin/python3 ' + os.path.dirname(os.path.abspath(__file__)) + '/' + 'stubborn_enable.py\n')
    ctfile.write('0 23 * * * /usr/bin/curl -X PUT -i \'http://' + args.ip_address + '/api/' + args.deconz_app_id + '/groups/2/action\' --data \'{"on": false}\'\n')



