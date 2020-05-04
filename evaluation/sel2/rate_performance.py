import json
from collections import defaultdict

import requests

token = '6a031facfd18b1133f11084293f89124251804e7'

headers = {'Accept': 'application/json',
           'Authorization': f'token {token}',
           'Content-Type': 'application/json'}

with open("failing_commits.json", "r") as fh:
    data = json.load(fh)

predictor_names = ['Original', 'AllRandom', 'AllInOrder', 'GreedyCoverAll', 'AffectedRandom', 'HGSAffected',
                   'GreedyCoverAffected',
                   'HGSAll', 'Alpha', 'Rocket', 'GreedyTimeAll']

csvdata = []
header = ["commit", "duration"]
header += predictor_names
header += [str(p) + "_ms" for p in predictor_names]
csvdata.append(header)

for run in data:
    print(run)
    parent = run['parent']

    # Get the test durations.
    try:
        with open(f"/media/pieter/data/thesistests/selab2-parentcoverages-parsed/{parent}-durations.json") as fh:
            parent_durations = json.load(fh)
    except:
        continue

    # Get the predictions.
    with open(f"/media/pieter/data/thesistests/selab2-predictions/{run['commit']}.json") as fh:
        predictions = json.load(fh)

    try:
        with open(f"/media/pieter/data/thesistests/selab2-testfailures-parsed/{run['commit']}-status.json") as fh:
            data = json.load(fh)
            all_tests = set(data.keys())
            failed_tests = set(k for k, v in data.items() if not v)
    except:
        continue

    if not failed_tests:
        failed_tests = all_tests

    first_failed_test = {}
    first_failed_test_ms = defaultdict(int)

    for predictor, prediction_str in predictions.items():
        prediction = prediction_str.split(',')

        for pi, test_case in enumerate(prediction):
            if test_case in failed_tests:
                first_failed_test[predictor] = pi
                break
            first_failed_test_ms[predictor] += int(parent_durations[test_case])

    original_sequence = set(parent_durations.keys()) | failed_tests
    original_sequence = list(sorted(original_sequence))

    original_first_failure = min(i for i, e in enumerate(original_sequence) if e in failed_tests)
    first_failed_test['Original'] = original_first_failure
    first_failed_test_ms['Original'] = sum(parent_durations[d] for d in original_sequence[:original_first_failure])

    for p in predictor_names:
        if p not in first_failed_test:
            first_failed_test[p] = -1
            first_failed_test_ms[p] = -1

    line = [run['commit'], str(sum(parent_durations.values()))]
    line += list(map(lambda p: str(first_failed_test[p]), predictor_names))
    line += list(map(lambda p: str(first_failed_test_ms[p]), predictor_names))
    csvdata.append(line)

with open("performance.csv", "w+") as fh:
    fh.writelines(f"{','.join(line)}\n" for line in csvdata)
