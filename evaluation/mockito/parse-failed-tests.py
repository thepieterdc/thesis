# Converts the csv file of BigQuery to a JSON file.

import csv
import json

with open('failed-tests.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)

    data = []

    for row in reader:
        data.append({
            'commit': row['tr_original_commit'],
            'build': int(row['tr_build_id']),
            'job': int(row['tr_jobs'].strip('[]')),
            'tests': row['tr_log_tests_failed'].split('#')
        })

    with open('failed-tests.json', 'w+') as fh:
        json.dump(data, fh)
