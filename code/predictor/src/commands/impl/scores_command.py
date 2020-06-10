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


class ScoresCommand(AbstractCommand):
    def __init__(self, db: AbstractDatabase):
        super().__init__(db)

    @staticmethod
    def name() -> str:
        return "scores"

    def run(self, arguments: List[str]) -> None:
        if not arguments:
            logging.error(f'Syntax: {self.name()} repository_url')
            exit(2)

        # Parse the arguments.
        repository_url = str(arguments[0]).rstrip("/")

        # Get the current repository.
        repository = self._db.get_repository(repository_url)
        if not repository:
            logging.error(f'Repository was not found.')
            exit(2)

        logging.info(f'Repository: {repository}')

        for (predictor, score) in self._db.get_scores(repository):
            logging.info(f'{predictor}: {score}')
