import json
import xml.etree.ElementTree as ET
from collections import defaultdict

import pyspark
from pyspark.sql import SparkSession


def parse_file_name(file_data):
    """
    (file, bytes)
    ->
    (commit, test, bytes)
    """
    commit = file_data[0][59:99]
    testname = file_data[0][109:-4]

    return commit, testname, file_data[1]


def parse_status(info_data):
    """
    (commit, test, bytes)
    ->
    (commit, {test: duration})
    """
    commit, test, coverage_bytes = info_data

    xml = ET.fromstring(coverage_bytes.decode("utf-8"))
    coverage = defaultdict(list)

    package: ET.Element
    for package in xml:
        if package.tag == 'package':
            pkg_folder = package.attrib['name']
            ch: ET.Element
            for ch in package:
                if ch.tag == 'sourcefile':
                    file = f"app/backend/src/main/java/{pkg_folder}/{ch.attrib['name']}"
                    fch: ET.Element
                    for fch in ch:
                        if fch.tag == "line":
                            if int(fch.attrib['ci']) > 0:
                                coverage[file].append(int(fch.attrib['nr']))

    return commit, {test: {'coverage': dict(coverage)}}


spark = SparkSession.builder.appName('thesis').getOrCreate()

# Set the log level.
sc = spark.sparkContext
sc.setLogLevel('INFO')

# Load the files into an RDD.
everything: pyspark.rdd = sc.binaryFiles("/media/pieter/data/thesistests/selab2-parentcoverages/**/coverage/*", minPartitions=100)

# Parse the filename.
files = everything.map(parse_file_name)

# Parse the status per commit/test.
parsed_status = files.map(parse_status)

# Group the statuses per commit/test.
grouped = parsed_status.reduceByKey(lambda a, b: {**a, **b})

for commit in grouped.collect():
    with open(f"/media/pieter/data/thesistests/selab2-parentcoverages-parsed/{commit[0]}-coverages.json", "w+") as fh:
        json.dump(commit[1], fh)
