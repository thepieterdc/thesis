# -*- coding: utf-8 -*-

"""Velocity predictors predictor."""
from typing import Set, Tuple, List

from src.entities.code_block import CodeBlock
from src.entities.test import Test
from src.predictors.abstract_predictor import AbstractPredictor

__author__ = "Pieter De Clercq"
__license__ = "MIT"


class RunAllTests(AbstractPredictor):
    """
    "Predictor" that simply executes all tests in order.
    """

    def predict(self, all_tests: Set[int],
                relevant_tests: Set[Tuple[Test, CodeBlock]]) -> List[int]:
        return list(sorted(all_tests))