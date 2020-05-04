import json
import xml.etree.ElementTree as ET

import pyspark
from pyspark.sql import SparkSession


def parse_file_name(file_data):
    """
    (file, bytes)
    ->
    (commit, test, bytes)
    """
    commit = file_data[0][59:99]
    testname = file_data[0][131:-4]

    return commit, testname, file_data[1]


def parse_status(info_data):
    """
    (commit, test, bytes)
    ->
    (commit, {test: duration})
    """
    commit, test_file, data = info_data

    xml = ET.fromstring(data.decode("utf-8"))

    el: ET.Element
    for el in xml:
        if el.tag == 'testcase':
            test_case = f"{test_file}.{el.attrib['name']}"
            yield commit, {test_case: int(float(el.attrib['time']) * 1000)}


spark = SparkSession.builder.appName('thesis').getOrCreate()

# Set the log level.
sc = spark.sparkContext
sc.setLogLevel('INFO')

# Load the files into an RDD.
everything: pyspark.rdd = sc.binaryFiles("/media/pieter/data/thesistests/selab2-parentcoverages/**/reports/**/*", minPartitions=100)

# Parse the filename.
files = everything.map(parse_file_name)

# Parse the status per commit/test.
parsed_status = files.flatMap(parse_status)

# Group the statuses per commit/test.
grouped = parsed_status.reduceByKey(lambda a, b: {**a, **b})

for commit in grouped.collect():
    with open(f"/media/pieter/data/thesistests/selab2-parentcoverages-parsed/{commit[0]}-durations.json", "w+") as fh:
        json.dump(commit[1], fh)
