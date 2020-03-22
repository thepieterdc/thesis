# -*- coding: utf-8 -*-

"""Velocity predictors predictor."""

__author__ = "Pieter De Clercq"
__license__ = "MIT"

from typing import Set, Iterable

from entities import Test
from predictors.abstract_predictor import AbstractPredictor


class AllInOrder(AbstractPredictor):
    """
    "Predictor" that simply executes all tests in order.
    """

    def __init__(self, all_tests: Set[Test]):
        """
        AllInOrder constructor.

        :param all_tests: all the tests
        """
        super().__init__(all_tests)

    def predict(self) -> Iterable[int]:
        return list(sorted(test.id for test in self.all_tests))
