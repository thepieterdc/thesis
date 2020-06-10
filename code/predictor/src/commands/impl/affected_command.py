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
        if len(arguments) != 2:
            logging.error(f'Syntax: {self.name()} repository_url commit')
            exit(2)

        # Parse the arguments.
        repository_url = str(arguments[0]).rstrip("/")
        commit = str(arguments[1])

        # Get the current repository.
        repository = self._db.get_repository(repository_url)
        if not repository:
            logging.error(f'Repository was not found.')
            exit(2)

        logging.info(f'Repository: {repository}')

        # Get the affected code in this commit.
        affected_code = list(repository.changes(commit))

        # Fetch the tests that cover the changed files.
        affected_tests = self._db.get_tests_by_coverage(repository, affected_code)

        affected_test_names = set(
            map(lambda t: self._db.get_test_by_id(t.id), affected_tests)
        )

        for test_case in sorted(affected_test_names):
            logging.info(f"{test_case}")
