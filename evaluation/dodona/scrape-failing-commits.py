import json

import requests

token = '6a031facfd18b1133f11084293f89124251804e7'

fails = []

pages = 50

headers = {'Accept': 'application/json',
           'Authorization': f'token {token}',
           'Content-Type': 'application/json'}

for page in range(1, pages):
    url = f"https://api.github.com/repos/dodona-edu/dodona/actions/workflows/ruby.yml/runs?page={page}"
    print(f"Fetching {url}")
    contents = requests.get(url, headers=headers).json()

    for run in filter(lambda r: r["conclusion"] == "failure", contents["workflow_runs"]):
        print(run['jobs_url'])
        commit = run['head_sha']
        jobs = requests.get(run['jobs_url'], headers=headers).json()
        for job in filter(lambda j: j["conclusion"] == "failure" and j["name"] == "test", jobs["jobs"]):
            # Find the first failed step.
            first = min(filter(lambda s: s["conclusion"] == "failure", job["steps"]), key=lambda j: j["number"])
            failed_step = first['name']

            if 'test' not in str(failed_step).lower():
                continue

            logs = requests.get(f'https://api.github.com/repos/dodona-edu/dodona/actions/jobs/{job["id"]}/logs',
                                headers=headers)
            with open(f"logs/{commit}.txt", "w+") as fh:
                fh.write(logs.text)

            fails.append({
                'commit': commit,
                'run': run['id'],
                'step': failed_step
            })

with open('failing_commits.json', 'w+') as fh:
    json.dump(fails, fh)
