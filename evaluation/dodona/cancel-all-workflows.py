import json

import requests

token = '6a031facfd18b1133f11084293f89124251804e7'

fails = []

pages = 50

headers = {'Accept': 'application/json',
           'Authorization': f'token {token}',
           'Content-Type': 'application/json'}

for page in range(1, pages):
    url = f"https://api.github.com/repos/thepieterdc/dodona-1/actions/runs?page={page}"
    print(f"Fetching {url}")
    contents = requests.get(url, headers=headers).json()
    for run in contents["workflow_runs"]:
        try:
            print(requests.post(f"https://api.github.com/repos/thepieterdc/dodona-1/actions/runs/{run['id']}/cancel", headers=headers).status_code)
        except:
            pass

        print(run['id'])
