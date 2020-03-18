# -*- coding: utf-8 -*-

"""Velocity predictors predictor."""

__author__ = "Pieter De Clercq"
__license__ = "MIT"

from collections import defaultdict
from typing import Tuple, Iterable, Generator, Set, Dict

from src.entities.code_block import CodeBlock
from src.predictors.abstract_predictor import AbstractPredictor


class GreedyCoverAffected(AbstractPredictor):
    """
    Predictor that ranks tests based on the amount of coverage
    they can provide.

    Greedy algorithm (Singh et al. 2016)
    """

    def __init__(self, affected_code: Iterable[CodeBlock],
                 all_tests: Dict[int, Set[CodeBlock]]):
        """
        GreedyCoverAffected constructor.

        :param affected_code: affected code blocks
        :param all_tests: all the tests
        """
        super().__init__()
        self.__affected_code = affected_code
        self.__all_tests = all_tests

    def predict(self) -> Generator[int, None, None]:
        # Create a map of the tests to their coverage lines.
        tests_lines = {
            test: set(line for line in cov)
            for test, covs in self.__all_tests.items() for cov in covs
        }

        # Create a set of coverage lines of the affected code.
        affected_lines = set(line for b in self.__affected_code for line in b)

        # Remove non-affected lines from the test lines.
        tests_lines = {t: v & affected_lines for (t, v) in tests_lines.items()}

        # While there are lines and tests remaining:
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
