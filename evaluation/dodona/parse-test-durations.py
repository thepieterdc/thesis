import json
import re

line_clear = re.compile(r"\.\d+Z(.*)")
test_name_regex = re.compile(r"(test_[^ ]+) ")
test_duration_regex = re.compile(r"PASS \((.*)s\)")

tests = {}

with open("test-durations.log", "r") as fh:
    line = fh.readline()

    while line and 'Started with run options' not in line:
        line = fh.readline()

    # Read the empty line.
    fh.readline()

    line = fh.readline()
    while line and 'Finished in ' not in line:
        test_name = line_clear.search(line).group(1).strip()

        line = fh.readline()
        while line and 'test_' in line:
            test_case = test_name_regex.search(line).group(1).strip()
            test_duration = test_duration_regex.search(line).group(1).strip()
            tests[f"{test_name}.{test_case}"] = float(test_duration)

            line = fh.readline()

        line = fh.readline()

with open('test-durations.json', 'w+') as fh:
    json.dump(tests, fh)
