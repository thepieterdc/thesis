# -*- coding: utf-8 -*-

"""Velocity predictors predictor."""

__author__ = "Pieter De Clercq"
__license__ = "MIT"

import logging
from typing import Set, Optional

from database.abstract_database import AbstractDatabase
from entities import Run
from predictors.abstract_predictor import AbstractPredictor
from predictors.impl.all_in_order import AllInOrder


class Evaluator:
    """
    An evaluator for predictions.
    """

    def __init__(self, database: AbstractDatabase,
                 predictors: Set[AbstractPredictor], run: Run, dry_run=False,
                 interactive=False, verbose=False):
        """
        Evaluator constructor.

        :param database: the database connection
        :param predictors: the predictors that should be evaluated
        :param run: the run
        :param dry_run: True if results should not be saved to the database
        :param interactive: True to interact with the user
        :param verbose: True to enable verbose logging
        """
        self.__database = database
        self.__dry_run = dry_run
        self.__interactive = interactive
        self.__predictors = predictors
        self.__run = run
        self.__verbose = verbose

    def evaluate(self):
        """
        Evaluates the predictors.
        """
        # Find the predictor.
        selected = self.__find_preferred_predictor()

        # Failsafe in case no predictor was found.
        if not selected or not self.__valid_predictor(selected):
            logging.info(selected)
            selected = AllInOrder.__name__

        # Make a prediction.
        for predictor in self.__predictors:
            # Get the name of the predictor.
            predictor_name = predictor.__class__.__name__
            predictor_selected = predictor_name == selected
            if self.__verbose:
                logging.info(f'Predictor: {predictor_name}')

            # Predict an order.
            order = list(predictor.predict())

            if self.__verbose:
                logging.info(f"Order predicted: {order}")
                logging.info("First 4 test names:")
                for t in order[:4]:
                    logging.info(self.__database.get_test_by_id(t))
                logging.info("")
                logging.info("")

            # Write the order to the database.
            if not self.__dry_run:
                self.__database.create_prediction(self.__run, predictor_name,
                                                  order, predictor_selected)

        # Mark the run as predicted.
        if not self.__dry_run:
            self.__database.run_predicted(self.__run)

    def __find_preferred_predictor(self) -> Optional[str]:
        """
        Gets the preferred predictor either from user input or from the
        database.

        :return: name of the selected predictor if any
        """
        if self.__dry_run:
            return None

        # Ask the user to provide a predictor.
        if self.__interactive:
            selected = None
            while not self.__valid_predictor(selected):
                selected = input("Preferred predictor: ")
            return selected

        # Find the preferred predictor in the database.
        return self.__database.get_preferred_predictor(
            self.__run.repository
        )

    def __valid_predictor(self, name: str) -> bool:
        """
        Gets whether the given predictor exists.

        :param name: the name of the predictor
        :return: true if the predictor exists
        """
        return any(p.__class__.__name__ == name for p in self.__predictors)
