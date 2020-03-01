#!/bin/sh

set -euxo

(cd ../ && ./gradlew --rerun-tasks jar publishToMavenLocal)

./gradlew velocity -i --rerun-tasks --stacktrace
