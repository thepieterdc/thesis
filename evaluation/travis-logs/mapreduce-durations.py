import json
from datetime import datetime
from operator import add
from typing import Tuple

import pyspark
from pyspark.sql import SparkSession

# Directory that contains the input tiles.
INPUT = '/media/pieter/data/thesistests/jobs/**.json'


def extract_start_end(file_and_data) -> Tuple[Tuple[str, str]]:
    """
    Parses the file and returns the start and end of every job.

    :param file_and_data: the file name and binary data
    :return: tuple of start and end time
    """
    data = json.loads(file_and_data[1])

    return tuple((str(d["started_at"]), str(d["finished_at"])) for d in data if d["state"] == "passed")


def parse_duration(start_end: Tuple[str, str]) -> int:
    """
    Parses the start and end timestamp to a duration.

    :param start_end: the start and end time
    :return: the duration
    """
    start = datetime.strptime(start_end[0], "%Y-%m-%dT%H:%M:%SZ")
    end = datetime.strptime(start_end[1], "%Y-%m-%dT%H:%M:%SZ")
    return int((end - start).total_seconds())


# Initialise a new Spark session.
spark = SparkSession.builder.appName('thesis').getOrCreate()

# Set the log level.
sc = spark.sparkContext
sc.setLogLevel('INFO')

# Load the data into an RDD.
files: pyspark.rdd = sc.binaryFiles(INPUT, minPartitions=10000)

# Parse the filename and find the start and end time for every file.
starts_ends = files.flatMap(extract_start_end)

# Calculate the duration for every timestamp.
durations = starts_ends.map(parse_duration)

with open("/home/pieter/PycharmProjects/untitled1/durations.txt", "w") as out:
    for duration in durations.collect():
        out.write(str(duration) + "\n")