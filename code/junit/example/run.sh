#!/bin/sh

set -euxo

(cd ../ && ./gradlew --rerun-tasks jar publishToMavenLocal)

./gradlew velocityTest -i --rerun-tasks --stacktrace -Pcommit="b87cc79da8aed7f1718eee24f0b75ff59774baae"
