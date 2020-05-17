import glob
import json
import xml.etree.ElementTree as ET
from collections import defaultdict


things = defaultdict(dict)

for f in glob.glob("/media/pieter/data/thesistests/d/**/reports/*.xml"):
    commit = f[33:73]
    testname = ':'.join(f[87:-4].rsplit('_', 1))

    test, line = testname.split(':')

    xml = ET.parse(f).getroot()

    success = int(xml.attrib['failures']) == 0 and int(xml.attrib['errors']) == 0
    filename = xml[0].attrib['file']
    patched_filename = filename + ':' + line

    testsuite = xml[0].attrib
    duration = int(float(testsuite['time']) * 1000)

    print(commit, patched_filename, duration, success)

    things[commit][patched_filename] = {'duration': duration, 'success': success}

for k, i in things.items():
    with open(f"/media/pieter/data/thesistests/dodona-results-parsed/{k}-statusduration.json", "w+") as fh:
        json.dump(i, fh)

print(things)

# spark = SparkSession.builder.appName('thesis').getOrCreate()
#
# # Set the log level.
# sc = spark.sparkContext
# sc.setLogLevel('INFO')
#
#
#
# # Load the files into an RDD.
# everything: pyspark.rdd = sc.binaryFiles("/media/pieter/data/thesistests/d/**/reports/*.xml", minPartitions=100)
#
# # Parse the filename.
# files = everything.map(parse_file_name)
#
# # Parse the status per commit/test.
# parsed_status = files.map(parse_status)
#
# # Group the statuses per commit/test.
# grouped = parsed_status.reduceByKey(lambda a, b: a + b)
#
# for commit in grouped.collect():
#     print(commit)
#     with open(f"/media/pieter/data/thesistests/dodona-results-parsed/{commit[0]}-statusduration.json", "w+") as fh:
#         json.dump(commit[1], fh)
