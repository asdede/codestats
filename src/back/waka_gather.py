import requests
from dotenv import load_dotenv
import os
import secrets

load_dotenv() # Temporary
secret = os.getenv('SECRET')

base_url = 'https://wakatime.com'

def get_user():
    users='/api/v1/users/current'
    res = request(users)

    info = {'name':res['display_name'],
            'created at': res['created_at'],
            'email': res['email']}
    return info

def get_all_time_data():
    all_time = '/api/v1/users/current/all_time_since_today'

    res = request(all_time)
    total_hours = {
        'time coded': res['text'],
        'start date': res['range']['start_date'],
        'end date': res['range']['end_date']
    }
    return total_hours

def get_editors():
    editors = '/api/v1/editors'
    res = request(editors)
    print(res)

durations = '/api/v1/users/current/durations'

def get_langs():
    languanges= '/api/v1/program_languages'
    res = request(languanges)
    return res

def get_stats():
    stats='/api/v1/users/current/stats'
    res = request(stats)
    daily_avg = res['human_readable_daily_average']
    systems = res['operating_systems']
    categories = res['categories']
    languanges = res['languages']
    total_hours = res['human_readable_total_including_other_language']
    editors = res['editors']
    stats = {}
    stats['daily average'] = daily_avg
    system_dict = {}
    for syst in systems:
        system_dict[syst['name']] = {'hours numeral':syst['decimal'], 'percent':syst['percent'], 'text':syst['text']}
    lang_stats = {}
    for lang in languanges:
        lang_stats[lang['name']] = {'hours numeral': lang['decimal'],'percent':lang['percent'], 'text':lang['text']}
    editor_stats = {}
    categor_stats = {}
    for cat in categories:
        categor_stats[cat['name']] = {'hours numeral': cat['decimal'],'percent':cat['percent'], 'text':cat['text']}
    for ed in editors:
        editor_stats[ed['name']] = {'hours numeral': ed['decimal'],'percent':ed['percent'], 'text':ed['text']}
    stats['total hours'] = total_hours
    stats['languanges'] = languanges
    stats['systems']= system_dict
    stats['categories'] = categor_stats
    stats['editors'] = editor_stats
    return stats

def get_weekly_stats():
    weekly_stats = '/api/v1/stats/last_7_days'
    #TODO


def request(req):
    res = requests.get(base_url+req,headers={'Authorization': f'Basic {secret}'}).json()
    return res['data']


commits = '/api/v1/users/current/projects/:project/commits/:hash'
data_dumps = '/api/v1/users/current/data_dumps'
editors = '/api/v1/editors'
external_durations = '/api/v1/users/current/external_durations'
beats = '/api/v1/users/current/heartbeats'
machine_names = '/api/v1/users/current/machine_names'
languanges= '/api/v1/program_languages'
projects= '/api/v1/users/current/projects'
stats='/api/v1/users/current/stats'
weekly_stats = '/api/v1/stats/last_7_days'
today_status_bar = '/api/v1/users/current/status_bar/today'


if __name__ == "__main__":
    get_stats()