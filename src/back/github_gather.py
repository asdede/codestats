import requests
from dotenv import load_dotenv
import os
base_url= 'https://api.github.com'
load_dotenv()
TOKEN = os.getenv('GITHUBSECRET')

def get_repos():
    url = f'{base_url}/user/repos'
    headers = {
    "Authorization": f"Bearer {TOKEN}"
    }
    res = requests.get(url,headers=headers)
    if res.status_code == 200:
        data = res.json()
    urls = []
    for d in data:
        urls.append(d['url'])
    return urls

def get_commits(url):
    s = '/commits'
    headers = {
    "Authorization": f"Bearer {TOKEN}"
    }
    res = requests.get(url+s,headers=headers).json()
    return len(res) if len(res) is not None else 0

def get_created_issues(url):
    s = '/issues'
    headers = {
    "Authorization": f"Bearer {TOKEN}"
    }
    params = {
        "filter": 'created',
        "state": "all"
    }
    res = requests.get(url+s,params=params,headers=headers).json()
    return len(res) if len(res) is not None else 0

def get_closed_issues(url):
    s = '/issues'
    headers = {
    "Authorization": f"Bearer {TOKEN}"
    }
    params = {
        "filter": 'mentioned',
        "state": "closed"
    }
    res = requests.get(url+s,params=params,headers=headers).json()
    return len(res) if len(res) is not None else 0

def main():
    "main method"
    repos = get_repos()
    total_commits, total_created_issues, total_closed_issues = 0,0,0
    for r in repos:
        total_commits += get_commits(r)
        total_created_issues += get_created_issues(r)
        total_closed_issues += get_closed_issues(r)
    print(total_commits, total_created_issues, total_closed_issues)
        

if __name__ == "__main__":
    main()