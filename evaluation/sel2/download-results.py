import os

import requests

token = '34179d64547d4b9fab8a254cef312d37b95324d6'

fails = []

pages = 50

headers = {'Accept': 'application/json',
           'Authorization': f'token {token}',
           'Content-Type': 'application/json'}

for page in range(1, 20):
    url = f"https://api.github.com/repos/Rostept/backend/actions/runs?page={page}&per_page=1000"
    print(f"Fetching {url}")
    contents = requests.get(url, headers=headers).json()

    for run in contents["workflow_runs"]:
        if 'coverage' in run['head_branch']:
            folder = "selab2-parentcoverages"
        else:
            folder = "selab2-testfailures"

        commit_name = run['head_branch'][:40]

        if os.path.exists(f"/media/pieter/data/thesistests/{folder}/{commit_name}.zip"):
            print(f"Already exists {commit_name}")
            continue

        if os.path.exists(f"/media/pieter/data/thesistests/{folder}/{commit_name}"):
            print(f"Already exists {commit_name}")
            continue

        print(f"Downloading {commit_name}")

        artifacts = requests.get(run['artifacts_url'], headers=headers).json()

        try:
            archive = requests.get(artifacts['artifacts'][0]['archive_download_url'], headers=headers)
            with open(f"/media/pieter/data/thesistests/{folder}/{commit_name}.zip", "wb") as f:
                f.write(archive.content)
        except:
            pass
