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


class PredictionsCommand(AbstractCommand):
    def __init__(self, db: AbstractDatabase):
        super().__init__(db)

    @staticmethod
    def name() -> str:
        return "predictions"

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

        for (predictor, prediction) in self._db.get_predictions(run):
            logging.info(f'Predictor: {predictor}')
            logging.info(f"[{', '.join(prediction)}]")
            logging.info("")
            logging.info("")
