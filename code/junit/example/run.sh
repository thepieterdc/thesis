#!/bin/sh

set -euxo

(cd ../ && ./gradlew --rerun-tasks jar publishToMavenLocal)

./gradlew velocityTest -i --rerun-tasks --stacktrace -Pcommit="ffa5a"
