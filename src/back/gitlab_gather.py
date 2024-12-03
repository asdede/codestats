from dotenv import load_dotenv
import os
import requests


load_dotenv()
name = os.getenv('gitlabname')
email = os.getenv('gitlabemail')
base_url = os.getenv('gitlaburl')
secret = os.getenv('GITLABSECRET')

def get_projects():
    url = f'{base_url}/api/v4/projects?owned=true'
    headers = {
        'Authorization': f'Bearer {secret}'
    }
    
    repo_ids = []
    page = 1  # Start with the first page

    while True:
        # Make a request with the current page
        response = requests.get(url=url, headers=headers, params={'page': page, 'per_page': 100})
        
        # Check for request errors
        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")
            break

        # Parse the JSON response
        data = response.json()
        if not data:  # If there's no data, we've reached the last page
            break

        for obj in data:

            repo_ids.append(obj['id'])
        
        page += 1
    
    return repo_ids

def get_issues():
    url = f'{base_url}/api/v4/issues_statistics'
    headers = {
        'Authorization': f'Bearer {secret}'
    }
    res = requests.get(url=url,headers=headers)
    return res.json()

def get_commits(id):
    url = f'{base_url}/api/v4/projects/{id}/repository/commits'
    headers = {
        'Authorization': f'Bearer {secret}'
    }
    
    commits_data = []
    page = 1  # Start with the first page

    while True:
        # Make a request with the current page
        response = requests.get(url=url, headers=headers, params={'page': page, 'per_page': 100})
        
        # Check for request errors
        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")
            break

        # Parse the JSON response
        data = response.json()
        if not data:  # If there's no data, we've reached the last page
            break

        for obj in data:
            commits_data.append(obj)
        
        page += 1

    return commits_data

def get_my_commits(commits):
    own_commits = []
    for c in commits:
        for i in c:
            if i['committer_name'] == name or i['author_email'] == email:
                own_commits.append(i)
    return own_commits


def get_merges(id):
    url = f'{base_url}/api/v4/projects/{id}/merge_requests?state=merged'
    headers = {
        'Authorization': f'Bearer {secret}'
    }
    
    merge_data = []
    page = 1  # Start with the first page

    while True:
        # Make a request with the current page
        response = requests.get(url=url, headers=headers, params={'page': page, 'per_page': 100})
        
        # Check for request errors
        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")
            break

        # Parse the JSON response
        data = response.json()
        if not data:  # If there's no data, we've reached the last page
            break

        for obj in data:
            merge_data.append(obj)
        
        page += 1

    return merge_data 
    
def main():
    project_ids = get_projects()
    commits = []
    merges = []
    for id in project_ids:
        commits.append(get_commits(id))
        merges.append(get_merges(id))
    own_commits = get_my_commits(commits)
    issue_stats = get_issues()

    stats = {
        'commits': len(own_commits),
        'total merges': len(merges),
        'created issues': issue_stats['statistics']['counts']['all'],
        'closed issues': issue_stats['statistics']['counts']['closed']
    }
    return stats

if __name__ == "__main__":
    main()