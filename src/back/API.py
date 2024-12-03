from fastapi import FastAPI
import json
from pydantic import BaseModel
from typing import List


class Skill(BaseModel):
    uuid: str
    key: str
    value: str
    category: str
    editable: bool

SKILLS_JSON_FILE = 'skills.json'

app = FastAPI()

def read_json(f_name):
    with open(f_name,'r') as f:
        return json.load(f)

def save_skills_to_file(skills):
    with open(SKILLS_JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(skills, f, indent=4)


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
    try:
        data = read_json('skills.json')
        return data
    except:
        return []

@app.post('/skills/add')
def save_skills(new_skills: List[Skill]):
    # Add new skills to the list
    new_skills_data = [skill.model_dump() for skill in new_skills]
    

    # Save updated skills back to the file
    save_skills_to_file(new_skills_data)