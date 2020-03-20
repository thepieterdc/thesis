#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Velocity predictors predictor."""

__author__ = "Pieter De Clercq"
__license__ = "MIT"

import logging
import sys

from database import PostgresDatabase
from predictors import AllInOrder, AllRandom, GreedyCoverAll, AffectedRandom, \
    GreedyCoverAffected, HGSAll, HGSAffected, Rocket, Alpha, GreedyTimeAll


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
predictors = [
    AffectedRandom(affected_tests),
    AllInOrder(all_tests),
    Alpha(all_tests, affected_tests, all_test_results),
    AllRandom(all_tests),
    GreedyCoverAffected(affected_code, all_tests),
    GreedyCoverAll(all_tests),
    GreedyCoverAll(all_tests),
    GreedyTimeAll(all_test_results),
    HGSAffected(affected_tests),
    HGSAll(all_tests),
    Rocket(all_test_results)
]
logging.info(
    f'Using {len(predictors)} available predictors: {", ".join(p.__class__.__name__ for p in predictors)}')

# Pick a predictor to use.
selected_predictor = ""
while not any(p.__class__.__name__ == selected_predictor for p in predictors):
    selected_predictor = input("Predictor? ")

# Make a prediction.
selected_order = []
for predictor in predictors:
    logging.info(f'Predictor: {predictor.__class__.__name__}')
    order = list(predictor.predict())
    logging.info(f"Order predicted: {order}")
    logging.info("First 4 test names:")
    for t in order[:4]:
        logging.info(db.get_test_by_id(t))
    logging.info("")
    logging.info("")
    logging.info("")
    if predictor.__class__.__name__ == selected_predictor:
        selected_order = order

# Save the prediction to the database.
db.update_run_set_order(run, selected_order)
logging.info('Order saved to the database.')
