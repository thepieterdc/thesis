#!/bin/sh

# Get the run id from the command line arguments.

python3 /app/src/cli.py "postgres://velocity:velocity@database:5432/velocity" $@
