import json

import docker
import requests

token = '6a031facfd18b1133f11084293f89124251804e7'

headers = {'Accept': 'application/json',
           'Authorization': f'token {token}',
           'Content-Type': 'application/json'}

with open("failing_tests.json", "r") as fh:
    failing_tests = json.load(fh)

client = docker.from_env()

for commit in failing_tests:
    hash = commit['commit']

    # Fetch the parent commit
    commit_req = requests.get(f'https://api.github.com/repos/dodona-edu/dodona/git/commits/{hash}',
                              headers=headers).json()

    try:
        print(hash, commit_req['parents'])
        parent = commit_req['parents'][0]['sha']

        # Find out whether the parent exists.
        branch_req = requests.get(f'https://api.github.com/repos/thepieterdc/dodona-analysis/branches?per_page=1000',
                                  headers=headers).json()
        branch_names = set(map(lambda b: b['name'], branch_req))

        if f'{parent}-instrument' in branch_names:
            print("Already exists")
            continue

        # Start a container.
        print(client.containers.run('dodona-instrumenter', f'/instrumenter.sh {parent}', remove=True))
    except Exception as e:
        print(e)
        print("FAILED")
        print(hash)
