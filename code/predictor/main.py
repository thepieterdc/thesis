#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Velocity order predictor."""

__author__ = "Pieter De Clercq"
__license__ = "MIT"

import logging
import sys

from src.database.postgres_database import PostgresDatabase

# Set-up the logger.
logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S',
                    level=logging.INFO)

if len(sys.argv) < 2:
    logging.error(f'Syntax: {sys.argv[0]} database_string run_id')
    exit(1)

if len(sys.argv) < 3:
    run_id = int(input("Run id: "))
else:
    run_id = int(sys.argv[2])

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
relevant_tests = list(db.get_tests_by_coverage(run, changes))
logging.info(f'Found {len(relevant_tests)} tests covering the changed files.')

# Determine the order in which the tests should be executed.
order = []
logging.info('Order determined.')

# Save the order to the database.
db.update_run_set_order(run, order)
logging.info('Order saved to the database.')
