#!/bin/sh

# Create a directory to store the coverage logs.
mkdir -p /tmp/run/coverage
mkdir -p /tmp/run/reports

# Download the jacoco cli.
curl -o /tmp/jacoco.zip -J -L "https://oss.sonatype.org/service/local/artifact/maven/redirect?r=snapshots&g=org.jacoco&a=jacoco&e=zip&v=LATEST"
unzip /tmp/jacoco.zip -d /tmp/jacoco

# Execute all tests to find all test names
./gradlew test

here=$(pwd)

# Save the duration times.
cp -r "$here/build/test-results" /tmp/run/reports

# Iterate over every file in the results directory.
find "/tmp/run/reports" -name "TEST-*.xml" | while read line; do
  # Parse the name of the class.
  classname=$(echo "$line" | egrep -o "TEST-.*.xml" | sed "s/TEST-//g" | sed "s/.xml$//g")

  # Find the tests in the class.
  egrep "testcase" "$line" | egrep -o " name=\"[^\"]*" | sed "s/^ name=\"//g" | while read testcase; do
    testname=$(echo "$classname.$testcase")
    ./gradlew test --tests "$testname"
    # Convert the coverage to xml.
    java -jar /tmp/jacoco/lib/jacococli.jar report "$here/build/jacoco/test.exec" --classfiles "$here/build/classes/" --xml "/tmp/run/coverage/$testname.xml"
  done
done
