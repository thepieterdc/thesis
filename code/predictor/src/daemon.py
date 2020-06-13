#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Velocity predictors predictor."""

__author__ = "Pieter De Clercq"
__license__ = "MIT"

import logging
import sys
from time import sleep

from database import PostgresDatabase
from predictors import create_all_predictors
from predictors.evaluator import Evaluator

# Set-up the logger.
logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S',
                    level=logging.INFO)

if len(sys.argv) < 2:
    logging.error(f'Syntax: {sys.argv[0]} database_string')
    exit(1)

# Create a database connection.
db = PostgresDatabase(sys.argv[1])
logging.info("Connected to the database.")

# Watch for runs that have not been predicted yet.
while True:
    run = db.get_unpredicted_run()
    if not run:
        sleep(1)
        continue

    logging.info(f'Run {run.id} found ({run.commit} @ {run.repository.url}).')

    # Get the affected code in this commit.
    affected_code = list(run.repository.changes(run.commit))

    # Fetch the tests that cover the changed files.
    affected_tests = db.get_tests_by_coverage(run.repository, affected_code)
    all_tests = db.get_tests(run.repository)
    all_test_results = db.get_test_results(run.repository)

    # Set-up the predictors.
    predictors = create_all_predictors(all_tests, affected_tests,
                                       all_test_results, affected_code)

    # Create an evaluator and evaluate the predictors.
    Evaluator(db, predictors, run).evaluate()

    logging.info(f'Run {run.id} predicted.')
