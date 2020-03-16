#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Velocity predictors predictor."""
from src.predictors.run_all_tests import RunAllTests

__author__ = "Pieter De Clercq"
__license__ = "MIT"

import logging
import sys

from src.database.postgres_database import PostgresDatabase


def get_run_id():
    """
    Gets the run id, either from the arguments or by asking it to the user.

    :return: the run id
    """
    if len(sys.argv) < 3:
        return int(input("Run id: "))
    return int(sys.argv[2])


# Set-up the logger.
logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S',
                    level=logging.INFO)

if len(sys.argv) < 2:
    logging.error(f'Syntax: {sys.argv[0]} database_string run_id')
    exit(1)

# Get the run id.
run_id = get_run_id()

# Create a database connection.
db = PostgresDatabase(sys.argv[1])
logging.info("Connected to the database.")

# Get the current run.
run = db.get_run_by_id(run_id)
if not run:
    logging.error(f'Run {run_id} was not found.')
    exit(2)

logging.info(f'Run found.')
logging.info(f'Repository: {run.repository}')

# Get the changes in this commit.
changes = list(run.repository.changes(run.commit))

# Fetch the tests that cover the changed files.
relevant_tests = set(db.get_tests_by_coverage(run, changes))
relevant_test_ids = set(test[0].id for test in relevant_tests)
all_tests = set(db.get_test_ids(run.repository))
logging.info(
    f"Found {len(relevant_test_ids)} tests covering the changed files, out of {len(all_tests)} total tests for this repository.")

# Set-up the predictors.
predictors = [RunAllTests()]
logging.info(f"Using {len(predictors)} available predictors.")

# Pick a predictor.
predictor = predictors[0]
logging.info(f"Chosen predictor: {predictor.__class__.__name__}")

# Make a prediction.
order = predictor.predict(all_tests, relevant_tests)

logging.info(f"Order predicted: {order}")

# Save the prediction to the database.
db.update_run_set_order(run, order)
logging.info('Order saved to the database.')
