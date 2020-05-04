import json

import docker
import requests

token = '34179d64547d4b9fab8a254cef312d37b95324d6'

headers = {'Accept': 'application/json',
           'Authorization': f'token {token}',
           'Content-Type': 'application/json'}

with open("failing_commits.json", "r") as fh:
    failing_tests = json.load(fh)

branches = set()
for i in range(1, 10):
    branch_req = requests.get(f'https://api.github.com/repos/Rostept/backend/branches?page={i}&per_page=1000',
                              headers=headers).json()
    branch_names = set(map(lambda b: b['name'], branch_req))
    branches |= branch_names

client = docker.from_env()

for commit in failing_tests:
    hash = commit['commit']

    try:
        print(hash)

        # Find out whether the commit exists.
        if f'{hash}-failures' in branches:
            print("Already exists")
            continue

        # Start a container.
        print(client.containers.run('sel2-instrumenter', f'/instrumenter.sh {hash}', remove=True))

        branches.add(f'{hash}-failures')
    except Exception as e:
        print(e)
        print("FAILED")
        print(hash)
