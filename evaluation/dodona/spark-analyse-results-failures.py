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
    commit = file_data[0][38:78]
    testname = ':'.join(file_data[0][87:-4].rsplit('_', 1))

    return commit, testname, file_data[1]


def parse_status(info_data):
    """
    (commit, test, bytes)
    ->
    (commit, {test: failure_status})
    """
    commit, test_no, data = info_data
    test, line = test_no.split(':')

    xml = ET.fromstring(data.decode("utf-8"))

    success = int(xml.attrib['failures']) == 0 and int(xml.attrib['errors']) == 0
    filename = xml[0].attrib['file']
    patched_filename = filename + ':' + line
    return commit, {patched_filename: success}


spark = SparkSession.builder.appName('thesis').getOrCreate()

# Set the log level.
sc = spark.sparkContext
sc.setLogLevel('INFO')

# Load the files into an RDD.
everything: pyspark.rdd = sc.binaryFiles("/media/pieter/data/thesistests/d/**/*", minPartitions=100)

# Parse the filename.
files = everything.map(parse_file_name)

# Parse the status per commit/test.
parsed_status = files.map(parse_status)

# Group the statuses per commit/test.
grouped = parsed_status.reduceByKey(lambda a, b: {**a, **b})

for commit in grouped.collect():
    with open(f"/media/pieter/data/thesistests/dodona-results-parsed/{commit[0]}-status.json", "w+") as fh:
        json.dump(commit[1], fh)
