# -*- coding: utf-8 -*-

"""Velocity predictors predictor."""

__author__ = "Pieter De Clercq"
__license__ = "MIT"

from typing import Iterable, Generator, Set

from entities import CodeBlock, Test
from predictors.abstract_predictor import AbstractPredictor


class GreedyCoverAffected(AbstractPredictor):
    """
    Predictor that ranks tests based on the amount of coverage
    they can provide.

    Greedy algorithm (Singh et al. 2016)
    """

    def __init__(self, affected_code: Iterable[CodeBlock],
                 all_tests: Set[Test]):
        """
        GreedyCoverAffected constructor.

        :param affected_code: affected code blocks
        :param all_tests: all the tests
        """
        super().__init__(all_tests)
        self.__affected_code = affected_code

    def predict(self) -> Generator[int, None, None]:
        # Create a map of the tests to their coverage lines.
        tests_lines = {
            test.id: set(line for line in cov)
            for test in self.all_tests for cov in test.coverage
        }

        # Store all tests.
        all_test_ids = set(t.id for t in self.all_tests)

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
            all_test_ids -= {max_test}

            # Mark the lines in the cover set of the test as covered.
            for test in tests_lines.keys():
                tests_lines[test] -= max_cov

        # Execute all remaining tests.
        for t in all_test_ids:
            yield t
