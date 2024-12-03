"""
Saves Github, gitlab and wakatime stats to 'cache', basicly to json.

This is planned to use in docker container. Everytime api is run, it gets these, and updates it to json files.

"""

from github_gather import main as hub_main
from gitlab_gather import main as lab_main
from waka_gather import get_stats, get_all_time_data
import time
import json

def save_to_json(data,f_name):
    with open(f_name,'w',encoding='utf-8') as f:
        f.write(json.dumps(data,indent=4))

def main():
    while True:
        time.sleep(60) # 1min
        print("Getting github data")
        hub_data = hub_main()
        print("Getting gitlab data")
        lab_data = lab_main()
        print("Getting wakatime stats")
        waka_data = get_stats()
        waka_hours = get_all_time_data()


        print("Saving to json")
        save_to_json(hub_data,'github.json')
        save_to_json(lab_data,'gitlab.json')
        save_to_json(waka_data,'wakatime.json')
        save_to_json(waka_hours,'wakatime_hours.json')
        print("Done!")
    
if __name__ == "__main__":
    main()



