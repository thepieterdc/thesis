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
    (commit, test, bytes)
    """
    commit = file_data[0][38:78]

    testname = ':'.join(file_data[0][88:-4].rsplit('_', 1))
    return commit, testname, file_data[1]


def parse_coverage(data):
    """
    (commit, test, coverage_bytes)
    ->
    ((commit), (test, coverage))
    """
    commit, test, coverage_bytes = data

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

    return commit, {test: {'coverage': dict(coverage)}}


spark = SparkSession.builder.appName('thesis').getOrCreate()

# Set the log level.
sc = spark.sparkContext
sc.setLogLevel('INFO')

# Load the files into an RDD.
everything: pyspark.rdd = sc.binaryFiles(
    "/media/pieter/data/thesistests/d/**/coverage/*.xml", minPartitions=100)

# Parse the filename.
files = everything.map(parse_file_name)

# Parse the coverage logs per commit/test.
parsed_coverages = files.map(parse_coverage)

# Parse the coverage logs per commit.
parsed_commits = parsed_coverages.reduceByKey(lambda a, b: {**a, **b})

for file in parsed_commits.collect():
    with open(f"/media/pieter/data/thesistests/dodona-results-parsed/{file[0]}-coverage.json", "w+") as fh:
        json.dump(file[1], fh)
