# -*- coding: utf-8 -*-

"""Velocity predictors predictor."""

__author__ = "Pieter De Clercq"
__license__ = "MIT"

import random
from typing import Set, Iterable

from src.predictors.abstract_predictor import AbstractPredictor


class AllRandom(AbstractPredictor):
    """
    "Predictor" that executes all tests in a randomised order.
    """

    def __init__(self, all_test_ids: Set[int]):
        """
        AllRandom constructor.

        :param all_test_ids: ids of all the tests
        """
        super().__init__()
        self.__all_test_ids = all_test_ids

    def predict(self) -> Iterable[int]:
        # Shuffle the list of all tests.
        tests = list(self.__all_test_ids)
        random.shuffle(tests)
        return tests
