import json

import requests

token = '5ef1cefe8569ddf4a7ebbba3d0956fbde3098e6b'

headers = {'Accept': 'application/json',
           'Authorization': f'token {token}',
           'Content-Type': 'application/json'}

with open("failing_commits.txt", "r") as fh:
    commits = list(l.strip() for l in fh.readlines())

fails = list()

for commit in commits:
    url = f"https://github.ugent.be/api/v3/repos/SoftwareEngineeringLab2/2017-2018-groep-05/commits/{commit}"
    print(f"Fetching {url}")
    contents = requests.get(url, headers=headers).json()

    try:
        parent = contents['parents'][0]['sha']
        statuses_url = f"https://github.ugent.be/api/v3/repos/SoftwareEngineeringLab2/2017-2018-groep-05/statuses/{parent}"
        statuses = requests.get(statuses_url, headers=headers).json()

        if any(status['state'] == 'success' and status['context'] == 'Test' for status in statuses):
            if any('app/backend/' in file['filename'] for file in contents['files']):
                fails.append({'commit': commit, 'parent': parent, 'changes': list(map(lambda f: f['filename'], contents['files']))})
    except:
        continue

with open("failing_commits.json", "w+") as fh:
    json.dump(fails, fh)