#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Velocity predictors predictor."""

__author__ = "Pieter De Clercq"
__license__ = "MIT"

import logging
import sys

from database import PostgresDatabase
from predictors import create_all_predictors
from predictors.evaluator import Evaluator


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

# Get the affected code in this commit.
affected_code = list(run.repository.changes(run.commit))

# Fetch the tests that cover the changed files.
affected_tests = db.get_tests_by_coverage(run, affected_code)
all_tests = db.get_tests(run.repository)
all_test_results = db.get_test_results(run.repository)
logging.info(
    f"Found {len(affected_tests)} tests covering the changed files, out of {len(all_tests)} total tests for this repository.")

# Set-up the predictors.
predictors = create_all_predictors(all_tests, affected_tests, all_test_results,
                                   affected_code)
logging.info(
    f'Using {len(predictors)} available predictors: {", ".join(p.__class__.__name__ for p in predictors)}')

# Ask whether to save the prediction to the database.
save_resp = input('Enter "SAVE" to save the results to the database: ').lower()
save = save_resp == 'save'
if save:
    logging.info('Results will be saved to the database.')
else:
    logging.info('Results will not be saved to the database.')

# Create an evaluator and evaluate the run.
Evaluator(db, predictors, run, not save, True, True).evaluate()
