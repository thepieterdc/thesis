# -*- coding: utf-8 -*-

"""Velocity predictors predictor."""

__author__ = "Pieter De Clercq"
__license__ = "MIT"

from typing import Set, Iterable, Tuple, Dict

from src.predictors.abstract_predictor import AbstractPredictor


class Rocket(AbstractPredictor):
    """
    Predictor that ranks all tests using the Rocket algorithm.

    ROCKET (Marijan et al. 2013)
    """

    def __init__(self, all_test_results: Dict[int, Tuple[bool]]):
        """
        Rocket constructor.

        :param all_test_results: results of all tests
        """
        super().__init__()
        self.__all_test_results = all_test_results

    def predict(self) -> Iterable[int]:
        return []
