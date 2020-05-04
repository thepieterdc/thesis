import json
from collections import defaultdict

import requests

token = '6a031facfd18b1133f11084293f89124251804e7'

headers = {'Accept': 'application/json',
           'Authorization': f'token {token}',
           'Content-Type': 'application/json'}

with open("performance.csv", "r") as fh:
    data = list(l.strip().split(',') for l in fh.readlines())

for i, run in enumerate(data[1:]):
    # Fetch the parent commit
    commit_req = requests.get(f'https://api.github.com/repos/dodona-edu/dodona/git/commits/{run[0]}',
                              headers=headers).json()

    parent = commit_req['parents'][0]['sha']

    # Get the test durations.
    with open(f"/media/pieter/data/thesistests/dodona-results-parsed/{parent}.json") as fh:
        parent_data = json.load(fh)

    durations = list(d['duration'] for d in parent_data.values())
    smin = list(sorted(durations))
    smax = list(reversed(smin))

    first_failure = int(run[2])
    min_time_to_failure = sum(smin[:first_failure])
    max_time_to_failure = sum(smax[:first_failure])
    avg_time_to_failure = (max_time_to_failure + min_time_to_failure) / 2.0

    run[13] = str(int(avg_time_to_failure))
    data[i + 1] = run

with open("performance-updated.csv", "w+") as fh:
    fh.writelines(f"{','.join(line)}\n" for line in data)
