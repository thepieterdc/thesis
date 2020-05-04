import json
from collections import defaultdict

import pyspark
from pyspark.sql import SparkSession

import xml.etree.ElementTree as ET

COVERAGE, REPORT = range(2)


def parse_file_name(file_data):
    """
    (file, bytes)
    ->
    (commit, test, type, bytes)
    """
    commit = file_data[0][38:78]
    type_ = COVERAGE if file_data[0][79:87] == 'coverage' else REPORT

    if type_ == COVERAGE:
        testname = ':'.join(file_data[0][88:-4].rsplit('_', 1))
    else:
        testname = ':'.join(file_data[0][87:-4].rsplit('_', 1))

    return (commit, testname), (type_, file_data[1])


def group_duration_coverage(type_and_data1, type_and_data2):
    """
    (COVERAGE, data1), (REPORT, data2)
    ->
    (data2, data1)
    """
    if type_and_data1[0] == COVERAGE:
        return type_and_data2[1], type_and_data1[1]
    else:
        return type_and_data1[1], type_and_data2[1]


def parse_duration(info_data):
    """
    ((commit, test), (duration_bytes, coverage_bytes))
    ->
    (commit, test, duration_ms, coverage_bytes)
    """
    info, data = info_data
    commit, test_no = info
    test, line = test_no.split(':')

    try:
        xml = ET.fromstring(data[0].decode("utf-8"))
    except Exception as e:
        print(info, data)
        exit(0)
    testsuite = xml[0].attrib
    filename = testsuite['file']
    duration = int(float(testsuite['time']) * 1000)

    patched_filename = filename + ':' + line
    return commit, patched_filename, duration, data[1]


def parse_coverage(data):
    """
    (commit, test, duration, coverage_bytes)
    ->
    ((commit), (test, duration_ms, coverage))
    """
    commit, test, duration_ms, coverage_bytes = data

    xml = ET.fromstring(coverage_bytes.decode("utf-8"))
    coverage = defaultdict(list)

    for package in xml[1]:
        cls: ET.Element
        for cls in package[0]:
            coverage_file_name = cls.attrib["filename"]

            line: ET.Element
            for line in cls[1]:
                number = int(line.attrib["number"])
                hits = int(line.attrib["hits"])
                if hits > 0:
                    coverage[coverage_file_name].append(number)

    return commit, {test: {'duration': duration_ms, 'coverage': dict(coverage)}}


spark = SparkSession.builder.appName('thesis').getOrCreate()

# Set the log level.
sc = spark.sparkContext
sc.setLogLevel('INFO')

# Load the files into an RDD.
everything: pyspark.rdd = sc.binaryFiles("/media/pieter/data/thesistests/d/**/*", minPartitions=100)

# Parse the filename.
files = everything.map(parse_file_name)

# Group the duration and coverage logs per commit/test.
duration_coverage = files.reduceByKey(group_duration_coverage)

# Parse the duration per commit/test.
parsed_duration = duration_coverage.map(parse_duration)

# Parse the coverage logs per commit/test.
parsed_coverages = parsed_duration.map(parse_coverage)

# Parse the coverage logs per commit.
parsed_commits = parsed_coverages.reduceByKey(lambda a, b: {**a, **b})

for file in parsed_commits.collect():
    with open(f"/media/pieter/data/thesistests/dodona-results-parsed/{file[0]}.json", "w+") as fh:
        json.dump(file[1], fh)
