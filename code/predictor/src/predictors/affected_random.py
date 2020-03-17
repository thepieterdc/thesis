# -*- coding: utf-8 -*-

"""Velocity predictors predictor."""

__author__ = "Pieter De Clercq"
__license__ = "MIT"

import random
from typing import Set, Iterable

from src.predictors.abstract_predictor import AbstractPredictor


class AffectedRandom(AbstractPredictor):
    """
    Predictor that executes only affected tests in a random order.
    """

    def __init__(self, affected_test_ids: Set[int]):
        """
        AffectedRandom constructor.

        :param affected_test_ids: ids of the affected tests
        """
        super().__init__()
        self.__affected_test_ids = affected_test_ids

    def predict(self) -> Iterable[int]:
        relevant_tests = list(self.__affected_test_ids)
        random.shuffle(relevant_tests)
        return relevant_tests
