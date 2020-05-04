#!/bin/sh

set -euxo

cd /app
commit=$1

git fetch origin $commit
git checkout $commit

# Copy the backend to a separate directory.
rm -rf /backend
cp -r /app/app/backend /backend

# Copy the workflow file.
mkdir -p /backend/.github/workflows
cp /workflow.yml /backend/.github/workflows/ci.yml

# Copy the runner.
cp /runner.sh /backend/runner.sh

cd /backend

# Remove stuff.
rm -rf /backend/simulatie
rm -rf /backend/run-backend.sh
rm /backend/database.md
rm /backend/sonar-project.properties

# Commit everything.
git config --global user.email "tim@localhost"
git config --global user.name "Tim"

git init
git checkout -b "$commit-failures"
git remote add analysis https://34179d64547d4b9fab8a254cef312d37b95324d6:x-oauth-basic@github.com/Rostept/backend.git
git add --all
git commit -a -m "$commit instrumented"
git push analysis +"$commit-failures"