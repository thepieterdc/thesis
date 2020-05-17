import json
from collections import defaultdict
import numpy as np
import requests

token = '6a031facfd18b1133f11084293f89124251804e7'

headers = {'Accept': 'application/json',
           'Authorization': f'token {token}',
           'Content-Type': 'application/json'}

with open("failing_tests.json", "r") as fh:
    data = json.load(fh)

predictor_names = ['Original', 'AllRandom', 'AllInOrder', 'GreedyCoverAll', 'AffectedRandom', 'HGSAffected', 'GreedyCoverAffected',
                   'HGSAll', 'Alpha', 'Rocket', 'GreedyTimeAll']

csvdata = []
header = ["commit", "duration"]
header += predictor_names
header += [str(p) + "_ms" for p in predictor_names]
csvdata.append(header)

for run in data:
    # Fetch the parent commit
    commit_req = requests.get(f'https://api.github.com/repos/dodona-edu/dodona/git/commits/{run["commit"]}',
                              headers=headers).json()

    parent = commit_req['parents'][0]['sha']

    if parent == '36faa6c373749890fbb75a752f7ef114709f627a':
        continue

    parent = '81d3f7cbde26504caadd69d6aaf0e6b215ad76d6'

    # Get the test durations.
    try:
        with open(f"/media/pieter/data/thesistests/dodona-results-parsed/{parent}.json") as fh:
            parent_data = json.load(fh)
    except:
        with open(f"/media/pieter/data/thesistests/dodona-results-parsed/{parent}-statusduration.json") as fh:
            parent_data = json.load(fh)

    parent_data = {k.split('/')[-1]: v for k, v in parent_data.items()}

    # Get the predictions.
    try:
        with open(f"/media/pieter/data/thesistests/dodona-predictions/{run['commit']}.json") as fh:
            predictions = json.load(fh)
    except FileNotFoundError:
        continue

    failed_tests = set(t.split('/')[-1] for t in run['tests'])

    first_failed_test = {}
    first_failed_test_ms = defaultdict(int)

    durations = list(d['duration'] for d in parent_data.values())
    avg_duration = np.median(durations)

    for predictor, prediction_str in predictions.items():
        prediction = prediction_str.split(',')
        prediction = [t.split('/')[-1] for t in prediction]

        for pi, test_case in enumerate(prediction):
            if test_case in failed_tests:
                first_failed_test[predictor] = pi
                break
            try:
                first_failed_test_ms[predictor] += int(parent_data[test_case]['duration'])
            except:
                first_failed_test_ms[predictor] += int(avg_duration)

    smin = list(sorted(durations))
    smax = list(reversed(smin))

    first_failure = min(i for i, e in enumerate(run['order']) if e != '.')
    min_time_to_failure = sum(smin[:first_failure])
    max_time_to_failure = sum(smax[:first_failure])
    avg_time_to_failure = (max_time_to_failure + min_time_to_failure) / 2.0

    first_failed_test['Original'] = first_failure
    first_failed_test_ms['Original'] = int(avg_time_to_failure)

    for p in predictor_names:
        if p not in first_failed_test:
            first_failed_test[p] = -1
            first_failed_test_ms[p] = -1

    print(first_failed_test)
    line = [run['commit'], str(sum(int(v['duration']) for v in parent_data.values()))]
    line += list(map(lambda p: str(first_failed_test[p]), predictor_names))
    line += list(map(lambda p: str(first_failed_test_ms[p]), predictor_names))
    csvdata.append(line)

with open("performance.csv", "w+") as fh:
    fh.writelines(f"{','.join(line)}\n" for line in csvdata)
