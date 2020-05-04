import json
from operator import add
from typing import Tuple

import pyspark
from pyspark.sql import SparkSession

# Directory that contains the input tiles.
INPUT = '/media/pieter/data/thesistests/jobs/**.json'


def parse_statuses(file_and_data) -> Tuple[str]:
    """
    Parses the file and returns the statuses of every job.

    :param file_and_data: the file name and binary data
    :return: tuple of statuses
    """
    data = json.loads(file_and_data[1])
    return tuple(str(d["state"]) for d in data)


# Initialise a new Spark session.
spark = SparkSession.builder.appName('thesis').getOrCreate()

# Set the log level.
sc = spark.sparkContext
sc.setLogLevel('INFO')

# Load the data into an RDD.
files: pyspark.rdd = sc.binaryFiles(INPUT, minPartitions=10000)

# Parse the filename and find the statuses for every file.
statuses = files.flatMap(parse_statuses)

# Count the status occurences.
counts = statuses.map(lambda x: (x, 1)).reduceByKey(add)

for status in counts.collect():
    print(status)