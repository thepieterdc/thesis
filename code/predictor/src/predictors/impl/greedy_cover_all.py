# -*- coding: utf-8 -*-

"""Velocity predictors predictor."""

__author__ = "Pieter De Clercq"
__license__ = "MIT"

from typing import Generator, Set

from entities import Test
from predictors.abstract_predictor import AbstractPredictor


class GreedyCoverAll(AbstractPredictor):
    """
    Predictor that ranks all tests based on the amount of additional coverage
    they can provide.

    Greedy algorithm (Singh et al. 2016)
    """

    def __init__(self, all_tests: Set[Test]):
        """
        GreedyCoverAll constructor.

        :param all_tests: all the tests
        """
        super().__init__(all_tests)

    def predict(self) -> Generator[int, None, None]:
        # Create a map of the tests to their coverage lines.
        tests_lines = {
            test.id: set(line for line in cov)
            for test in self.all_tests for cov in test.coverage
        }

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
