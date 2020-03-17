# -*- coding: utf-8 -*-

"""Velocity predictors predictor."""

__author__ = "Pieter De Clercq"
__license__ = "MIT"

from typing import Set, Iterable

from src.predictors.abstract_predictor import AbstractPredictor


class AllInOrder(AbstractPredictor):
    """
    "Predictor" that simply executes all tests in order.
    """

    def __init__(self, all_test_ids: Set[int]):
        """
        AllInOrder constructor.

        :param all_test_ids: ids of all the tests
        """
        super().__init__()
        self.__all_test_ids = all_test_ids

    def predict(self) -> Iterable[int]:
        return list(sorted(self.__all_test_ids))
