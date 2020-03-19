# -*- coding: utf-8 -*-

"""Velocity predictors predictor."""

__author__ = "Pieter De Clercq"
__license__ = "MIT"

import random
from typing import Set, Iterable

from entities import Test
from src.predictors.abstract_predictor import AbstractPredictor


class AllRandom(AbstractPredictor):
    """
    "Predictor" that executes all tests in a randomised order.
    """

    def __init__(self, all_tests: Set[Test]):
        """
        AllRandom constructor.

        :param all_tests: all the tests
        """
        super().__init__()
        self.__all_tests = all_tests

    def predict(self) -> Iterable[int]:
        # Shuffle the list of all tests.
        tests = list(test.id for test in self.__all_tests)
        random.shuffle(tests)
        return tests
