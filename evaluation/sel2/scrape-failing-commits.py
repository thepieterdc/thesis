import json

import requests

token = '5ef1cefe8569ddf4a7ebbba3d0956fbde3098e6b'

fails = []

pages = 100

headers = {'Accept': 'application/json',
           'Authorization': f'token {token}',
           'Content-Type': 'application/json'}

failed_tests = set()

for page in range(1, pages):
    url = f"https://github.ugent.be/api/v3/repos/SoftwareEngineeringLab2/2017-2018-groep-05/commits?page={page}&per_page=1000"
    print(f"Fetching {url}")
    contents = requests.get(url, headers=headers).json()

    for commit in contents:
        commit_hash = commit['sha']
        statuses_url = f"https://github.ugent.be/api/v3/repos/SoftwareEngineeringLab2/2017-2018-groep-05/statuses/{commit_hash}"
        statuses = requests.get(statuses_url, headers=headers).json()

        if any(status['state'] == 'error' and status['context'] == 'Test' for status in statuses):
            if (any(status['state'] == 'success' and status['context'] == 'Build' for status in statuses)):
                with open("failing_commits.txt", "a+") as fh:
                    fh.write(f"{commit_hash}\n")
