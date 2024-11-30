import requests
from dotenv import load_dotenv
import os
from hashlib import sha256
import secrets


load_dotenv()
base_url = 'https://wakatime.com'
users='/api/v1/users/current'
all_time = '/api/v1/users/current/all_time_since_today'
commits = '/api/v1/users/current/projects/:project/commits/:hash'
data_dumps = '/api/v1/users/current/data_dumps'
durations = '/api/v1/users/current/durations'
editors = '/api/v1/editors'
external_durations = '/api/v1/users/current/external_durations'
beats = '/api/v1/users/current/heartbeats'
machine_names = '/api/v1/users/current/machine_names'
languanges= '/api/v1/program_languages'
projects= '/api/v1/users/current/projects'
stats='/api/v1/users/current/stats'
weekly_stats = '/api/v1/stats/last_7_days'
today_status_bar = '/api/v1/users/current/status_bar/today'
salt = secrets.token_hex(16)
secret = os.getenv('SECRET')
m = sha256((secret+salt).encode()).hexdigest()
print(m)
res = requests.get(base_url+today_status_bar,headers={'Authorization': f'Basic {secret}'})
print(res.status_code)
print(res.text)