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
    commit = file_data[0][56:96]
    testname = file_data[0][120:-4]

    return commit, testname, file_data[1]


def parse_status(info_data):
    """
    (commit, test, bytes)
    ->
    (commit, {test: failure_status})
    """
    commit, test_file, data = info_data

    xml = ET.fromstring(data.decode("utf-8"))

    el: ET.Element
    for el in xml:
        if el.tag == 'testcase':
            test_case = f"{test_file}.{el.attrib['name']}"
            yield commit, {test_case: not (any(e.tag == 'failure' or e.tag == 'error' for e in el))}


spark = SparkSession.builder.appName('thesis').getOrCreate()

# Set the log level.
sc = spark.sparkContext
sc.setLogLevel('INFO')

# Load the files into an RDD.
everything: pyspark.rdd = sc.binaryFiles("/media/pieter/data/thesistests/selab2-testfailures/**/**/*", minPartitions=100)

# Parse the filename.
files = everything.map(parse_file_name)

# Parse the status per commit/test.
parsed_status = files.flatMap(parse_status)

# Group the statuses per commit/test.
grouped = parsed_status.reduceByKey(lambda a, b: {**a, **b})

for commit in grouped.collect():
    with open(f"/media/pieter/data/thesistests/selab2-testfailures-parsed/{commit[0]}-status.json", "w+") as fh:
        json.dump(commit[1], fh)
