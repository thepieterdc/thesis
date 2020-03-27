#!/bin/sh

mkdir -p /tmp/run/coverage
mkdir -p /tmp/run/reports

egrep -rn "^\s+test " test/ | egrep -o 'test/[^:]+:[0-9]+' | while read line; do
  echo "$line"
  DATABASE_URL="mysql2://root:dodona@mysql:3306/dodona_test" bundle exec rails test "$line" || true
  name=$(echo "$line" | sed "s/:/_/")
  name=$(basename "$name")
  mv 'coverage/coverage.xml' "/tmp/run/coverage/$name.xml" || true
  mv test/reports/* "/tmp/run/reports/$name.xml" || true
done
