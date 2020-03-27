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
#
# # Parse the filename and find the average gradient for every image.
# images_with_gradient = images.map(parse_avg_gradient)
#
# # Reduce by taking the highest average gradient per x/y/cycle/channel.
# highest_average_gradient = images_with_gradient.reduceByKey(
#     lambda a, b: a if a[0] > b[0] else b
# )
#
# # Reorder the values to group them by cycle/channel, throw away unnecessary
# # information and create a matrix to reduce in the next step.
# best_by_cycle_channel = highest_average_gradient.map(
#     lambda image: group_by_cycle_and_channel(image, MATRIX_SHAPE)
# )
#
# # Reduce all rows of the same cycle and channel into a matrix that contains the
# # non-zero elements of both matrices.
# cycle_channel_images = best_by_cycle_channel.reduceByKey(
#     lambda first, second: np.where(first, first, second)
# )
#
# # Crop the matrix to the present elements.
# cropped_images = cycle_channel_images.map(crop_image)
#
# # Replace the file names by actual image data.
# restored_images = cropped_images.map(
#     lambda image: restore_image(image, TILE_SHAPE)
# )
#
# # Save every image to a tif file.
# for image in restored_images.collect():
#     (cycle, channel), data = image
#
#     # Devise a file name, save the image as png, might need to save this to
#     # tiff later on.
#     file_name = f'{OUTPUT}/cyc_{cycle}_chan_{channel}.tiff'
#
#     # Write the file data.
#     data_image = Image.fromarray(data)
#     data_image.save(file_name)
