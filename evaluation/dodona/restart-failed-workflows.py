import json

import docker
import requests

token = '6a031facfd18b1133f11084293f89124251804e7'

headers = {'Accept': 'application/json',
           'Authorization': f'token {token}',
           'Content-Type': 'application/json'}
pages = 50
for page in range(1, pages):
    url = f"https://api.github.com/repos/thepieterdc/dodona-analysis/actions/workflows/ruby.yml/runs?page={page}"
    print(f"Fetching {url}")
    contents = requests.get(url, headers=headers).json()

    for run in filter(lambda r: r["conclusion"] == "failure", contents["workflow_runs"]):
        jobs = requests.get(run['jobs_url'], headers=headers).json()
        fails = set((j["name"], j["id"]) for j in jobs["jobs"] if j["conclusion"] == 'failure')
        print(fails)
        for fail_name, fail_id in fails:
            if fail_name == 'test':
                logs = requests.get(
                    f'https://api.github.com/repos/thepieterdc/dodona-analysis/actions/jobs/{fail_id}/logs',
                    headers=headers).text
                if 'fatal: reference is not a tree' in logs:
                    print(requests.post(
                        f'https://api.github.com/repos/thepieterdc/dodona-analysis/actions/runs/{run["id"]}/rerun',
                        headers=headers).json())
