# -*- coding: utf-8 -*-

"""Velocity predictors predictor."""

__author__ = "Pieter De Clercq"
__license__ = "MIT"

import random
from typing import Set, Iterable

from entities import Test
from predictors.abstract_predictor import AbstractPredictor


class AffectedRandom(AbstractPredictor):
    """
    Predictor that executes only affected tests in a random order.
    """

    def __init__(self, affected_tests: Set[Test]):
        """
        AffectedRandom constructor.

        :param affected_tests: the affected tests
        """
        super().__init__()
        self.__affected_tests = affected_tests

    def predict(self) -> Iterable[int]:
        relevant_tests = list(test.id for test in self.__affected_tests)
        random.shuffle(relevant_tests)
        return relevant_tests
