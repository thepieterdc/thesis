# -*- coding: utf-8 -*-

"""Velocity CLI command."""

__author__ = "Pieter De Clercq"
__license__ = "MIT"

import logging
from typing import Iterable, List

from commands.abstract_command import AbstractCommand
from database.abstract_database import AbstractDatabase
from predictors import create_all_predictors
from predictors.evaluator import Evaluator


class PredictCommand(AbstractCommand):
    def __init__(self, db: AbstractDatabase):
        super().__init__(db)

    @staticmethod
    def name() -> str:
        return "predict"

    def run(self, arguments: List[str]) -> None:
        if not arguments:
            logging.error(f'Syntax: {self.name()} run_id')
            exit(2)

        # Parse the arguments.
        run_id = int(arguments[0])

        # Get the current run.
        run = self._db.get_run_by_id(run_id)
        if not run:
            logging.error(f'Run {run_id} was not found.')
            exit(2)

        logging.info(f'Run found.')
        logging.info(f'Repository: {run.repository}')

        # Get the affected code in this commit.
        affected_code = list(run.repository.changes(run.commit))

        # Fetch the tests that cover the changed files.
        affected_tests = self._db.get_tests_by_coverage(run, affected_code)
        all_tests = self._db.get_tests(run.repository)
        all_test_results = self._db.get_test_results(run.repository)
        logging.info(
            f"Found {len(affected_tests)} tests covering the changed files, out of {len(all_tests)} total tests for this repository.")

        # Set-up the predictors.
        predictors = create_all_predictors(all_tests, affected_tests,
                                           all_test_results,
                                           affected_code)
        logging.info(
            f'Using {len(predictors)} available predictors: {", ".join(p.__class__.__name__ for p in predictors)}')

        # Ask whether to save the prediction to the database.
        save_resp = input(
            'Enter "SAVE" to save the results to the database: ').lower()
        save = save_resp == 'save'
        if save:
            logging.info('Results will be saved to the database.')
        else:
            logging.info('Results will not be saved to the database.')

        # Create an evaluator and evaluate the run.
        Evaluator(self._db, predictors, run, not save, True, True).evaluate()
