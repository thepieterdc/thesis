import os

import requests

token = '6a031facfd18b1133f11084293f89124251804e7'

fails = []

pages = 50

headers = {'Accept': 'application/json',
           'Authorization': f'token {token}',
           'Content-Type': 'application/json'}

for page in range(1, 10):
    url = f"https://api.github.com/repos/thepieterdc/dodona-analysis/actions/runs?page={page}"
    print(f"Fetching {url}")
    contents = requests.get(url, headers=headers).json()
    for run in contents["workflow_runs"]:
        if 'instrument' not in run['head_branch']:
            print(f"Skipped {run['head_branch']}")
            continue

        commit_name = run['head_branch'][:40]

        if os.path.exists(f"/media/pieter/data/thesistests/d/{commit_name}.zip"):
            print(f"Already exists {commit_name}")
            continue

        if os.path.exists(f"/media/pieter/data/thesistests/d/{commit_name}"):
            print(f"Already exists {commit_name}")
            continue

        if run['conclusion'] == 'cancelled':
            continue

        print(run)

        print(f"Downloading {commit_name}")

        artifacts = requests.get(run['artifacts_url'], headers=headers).json()

        if artifacts['total_count'] != 1:
            print(f"Artifacts in {commit_name}: {','.join(str(artifacts['artifacts']))}")

        try:
            archive = requests.get(artifacts['artifacts'][0]['archive_download_url'], headers=headers)
            with open(f"/media/pieter/data/thesistests/d/{commit_name}.zip", "wb") as f:
                f.write(archive.content)
        except:
            pass
