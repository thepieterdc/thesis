# -*- coding: utf-8 -*-

"""Velocity predictors predictor."""

__author__ = "Pieter De Clercq"
__license__ = "MIT"

import operator
from collections import defaultdict
from functools import reduce
from typing import Tuple, Iterable, Generator, Set, Dict

from entities import CodeBlock, Test, TestResult
from predictors.abstract_predictor import AbstractPredictor


class GreedyTimeAll(AbstractPredictor):
    """
    Predictor that orders tests based on their execution duration. This
    algorithm considers all tests. Tests that have not yet been executed before
    are omitted.
    """

    def __init__(self, test_results: Dict[int, Tuple[TestResult]]):
        """
        GreedyTimeAll constructor.

        :param test_results: results of every test
        """
        super().__init__()
        self.__test_results = test_results

    def average_duration(self, results: Tuple[TestResult]) -> int:
        """
        Calculates the average test duration in nanoseconds.

        :param results: the results of the test
        :return: the average duration
        """
        # Find whether this test has ever been successful.
        if any(not t.failed for t in results):
            candidates = filter(lambda t: not t.failed, results)
        else:
            candidates = results

        # Find the average duration over all executions.
        total_duration = reduce(
            lambda acc, r: (acc[0] + r.duration, acc[1] + 1),
            candidates,
            (0, 0)
        )

        return total_duration[0] / total_duration[1]

    def predict(self) -> Generator[int, None, None]:
        # Find the average duration per test.
        test_durations = (
            (t, self.average_duration(v)) for t, v in
            self.__test_results.items()
        )

        # Return the tests sorted on their duration.
        for test in sorted(test_durations, key=operator.itemgetter(1)):
            yield test[0]
