import json
import os
import re

with open("failing_commits.json", "r") as fh:
    failed_commits = json.load(fh)

with open('failing_tests.json', 'r+') as fh:
    fails = json.load(fh)

processed_fails = set(f['commit'] for f in fails)

failures_regex = re.compile(r"Z (.*)")
line_regex = re.compile(r"rails test (test/.*:\d+)")

for failing_commit in failed_commits:
    if failing_commit['commit'] in processed_fails:
        continue

    log_file = f"logs/{failing_commit['commit']}.txt"
    if not os.path.exists(log_file):
        continue

    with open(log_file, "r") as fh:
        line = fh.readline()
        while line and 'Running:' not in line and 'Aborted (core dumped)' not in line and "Table 'dodona_test.users' doesn't exist" not in line and "Can't connect to MySQL server" not in line and 'SimpleCov failed with exit 1' not in line and 'failed to load command: rails' not in line:
            line = fh.readline()

        if 'Aborted (core dumped)' in line or "Table 'dodona_test.users' doesn't exist" in line or "Can't connect to MySQL server" in line:
            continue

        if 'SimpleCov failed with exit 1' in line or 'failed to load command: rails' in line:
            continue

        # Read the empty line.
        fh.readline()

        failures = fh.readline()

        print(failing_commit)

        failures = failures_regex.search(failures).group(1)

        while line and 'Failed Tests:' not in line:
            line = fh.readline()

        if not line:
            continue

        # Move to the empty line.
        fh.readline()

        # Move to the first test.
        line = fh.readline()
        failing_tests = []
        while 'bin/rails test' in line:
            failing_test = line_regex.search(line).group(1)
            failing_tests.append(failing_test)

            line = fh.readline()

        fails.append({
            'commit': failing_commit['commit'],
            'order': failures,
            'tests': failing_tests
        })

with open('failing_tests.json', 'w+') as fh:
    json.dump(fails, fh)
