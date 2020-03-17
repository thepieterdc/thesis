# -*- coding: utf-8 -*-

"""Velocity predictors predictor."""
import operator
from collections import defaultdict

__author__ = "Pieter De Clercq"
__license__ = "MIT"

import random
from typing import Set, Tuple, Iterable, Generator

from src.entities.code_block import CodeBlock
from src.entities.test import Test
from src.predictors.abstract_predictor import AbstractPredictor


class GreedyCoverAll(AbstractPredictor):
    """
    Predictor that ranks all tests based on the amount of additional coverage
    they can provide.

    Greedy algorithm (Singh et al. 2016)
    """

    def __init__(self, all_tests: Iterable[Tuple[int, CodeBlock]]):
        """
        GreedyCoverAll constructor.

        :param all_tests: all the tests
        """
        super().__init__()
        self.__all_tests = all_tests

    def predict(self) -> Generator[int, None, None]:
        # Create a map of the tests to their coverage lines.
        tests_lines = defaultdict(set)
        for (test, cov) in self.__all_tests:
            for line in cov:
                tests_lines[test].add(line)

        # While there are tests remaining:
        while tests_lines:
            # Find the test that adds the most uncovered lines. This needs to be
            # computed twice to guarantee a deterministic order.
            max_cov_amt = max(len(val) for val in tests_lines.values())
            max_test, max_cov = max(
                i for i in tests_lines.items() if len(i[1]) == max_cov_amt,
            )

            # Return the test.
            del tests_lines[max_test]
            yield max_test

            # Mark the lines in the cover set of the test as covered.
            for test in tests_lines.keys():
                tests_lines[test] -= max_cov

            # Remove tests that do not add any additional coverage.
            tests_lines = {t: v for (t, v) in tests_lines.items() if v}
