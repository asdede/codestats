from fastapi import FastAPI
import json

app = FastAPI()

def read_json(f_name):
    with open(f_name,'r') as f:
        return json.load(f)

@app.get('/stats/github')
def get_github_stats():
    data = read_json('github.json')
    return data

@app.get('/stats/gitlab')
def get_gitlab_stats():
    data = read_json('gitlab.json')
    return data

@app.get('/stats/wakatime')
def get_wakatime_stats():
    data = read_json('wakatime.json')
    return data

@app.get('/stats/wakatime/hours')
def get_wakatime_hours():
    data = read_json('wakatime_hours.json')
    return data

@app.get('/skills')
def get_skills():
    data = read_json('skills.json')
    return data