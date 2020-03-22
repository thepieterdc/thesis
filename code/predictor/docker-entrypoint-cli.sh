#!/bin/sh

# Get the run id from the command line arguments.
run_id="$1"

python3 /app/src/main.py "postgres://velocity:velocity@database:5432/velocity" $run_id
