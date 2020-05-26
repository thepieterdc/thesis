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


class DurationsCommand(AbstractCommand):
    def __init__(self, db: AbstractDatabase):
        super().__init__(db)

    @staticmethod
    def name() -> str:
        return "durations"

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

        test_results = self._db.get_test_results(run.repository)

        test_cases = {k: mean(tuple(r.duration for r in v)) for k, v in
                      test_results.items()}

        for test_case in sorted(test_cases.items(), key=lambda a: a[1],
                                reverse=True):
            test_id, duration = test_case
            logging.info(f"{self._db.get_test_by_id(test_id)}: {duration}ms")
