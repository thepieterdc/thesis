import json

import requests

token = '34179d64547d4b9fab8a254cef312d37b95324d6'

fails = []

pages = 50

headers = {'Accept': 'application/json',
           'Authorization': f'token {token}',
           'Content-Type': 'application/json'}

for page in range(1, pages):
    url = f"https://api.github.com/repos/Rostept/backend/actions/runs?page={page}"
    print(f"Fetching {url}")
    contents = requests.get(url, headers=headers).json()
    for run in contents["workflow_runs"]:
        try:
            print(requests.post(f"https://api.github.com/repos/Rostept/backend/actions/runs/{run['id']}/cancel", headers=headers).status_code)
        except:
            pass

        print(run['id'])
