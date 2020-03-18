# -*- coding: utf-8 -*-

"""Velocity predictors predictor."""

__author__ = "Pieter De Clercq"
__license__ = "MIT"

import operator
from collections import defaultdict
from typing import Generator, Set, Dict, Tuple

from entities import CodeBlock, CodeLine, Test
from predictors.abstract_predictor import AbstractPredictor


class HGSAffected(AbstractPredictor):
    """
    Predictor that ranks the affected tests using the HGS algorithm.

    HGS algorithm (Harrold et al. 1993)
    """

    def __init__(self, affected_tests: Dict[Test, Set[CodeBlock]]):
        """
        HGSAll constructor.

        :param affected_tests: the affected tests
        """
        super().__init__()
        self.__affected_tests = affected_tests

    def predict(self) -> Generator[int, None, None]:
        # Create a map of the code lines to their tests.
        lines_tests = defaultdict(set)
        for (test, covs) in self.__affected_tests.items():
            test_cov_lines = sum(len(cov) for cov in covs)
            for cov in covs:
                for line in cov:
                    lines_tests[line].add((test, test_cov_lines))

        # Reduce the amount of lines by joining mutual sets.
        test_requirements = set(self.__reduce_requirements(lines_tests))

        # Store the tests that should be executed.
        ret = set()

        # While there are test requirements left.
        while test_requirements:
            # Find the minimal cardinality.
            min_card = min(len(t) for t in test_requirements)

            # Find the sets with minimal cardinality.
            min_sets = {t[0] for t in test_requirements if len(t) == min_card}
            min_sets_ids = {t[0] for t in min_sets}

            ret |= min_sets

            # Remove the returned sets from the requirements.
            test_requirements = set(filter(lambda t: t, {
                tuple(t for t in req if t[0] not in min_sets_ids)
                for req in test_requirements
            }))

        # Return all the t sets ordered on their cardinality.
        for t in sorted(ret, key=operator.itemgetter(1), reverse=True):
            yield t[0].id

    @staticmethod
    def __reduce_requirements(lines: Dict[CodeLine, Set[Tuple[int, int]]]) -> \
        Generator[Tuple[Tuple[int, int]], None, None]:
        """
        Reduces the test lines to group mutual coverage sets.

        :param lines: the input lines
        :return: reduced set
        """
        # Mutually exclusive cover sets.
        lines_to_check = set(lines.keys())

        # While there are lines left to check.
        while lines_to_check:
            # Pick a random line.
            line = next(iter(lines_to_check))
            tests = lines[line]

            # Return the tests.
            yield tuple(tests)

            # Remove the line from the lines left to check.
            lines_to_check -= {line}

            # Find all lines with the same coverage set and remove them from the
            # remaining list.
            lines_to_check -= {l for l, lt in lines.items() if lt == tests}
