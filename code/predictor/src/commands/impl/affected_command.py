# -*- coding: utf-8 -*-

"""Velocity CLI command."""

__author__ = "Pieter De Clercq"
__license__ = "MIT"

import logging
from typing import Iterable, List

from numpy import mean

from commands.abstract_command import AbstractCommand
from database.abstract_database import AbstractDatabase
from predictors import create_all_predictors
from predictors.evaluator import Evaluator


class AffectedCommand(AbstractCommand):
    def __init__(self, db: AbstractDatabase):
        super().__init__(db)

    @staticmethod
    def name() -> str:
        return "affected"

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

        affected_test_names = set(
            map(lambda t: self._db.get_test_by_id(t.id), affected_tests)
        )

        for test_case in sorted(affected_test_names):
            logging.info(f"{test_case}")
