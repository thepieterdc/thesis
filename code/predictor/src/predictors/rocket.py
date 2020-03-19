# -*- coding: utf-8 -*-

"""Velocity predictors predictor."""

__author__ = "Pieter De Clercq"
__license__ = "MIT"

import operator
from typing import Set, Iterable, Tuple, Dict

from entities import TestResult
import numpy as np
from predictors.abstract_predictor import AbstractPredictor


class Rocket(AbstractPredictor):
    """
    Predictor that ranks all tests using the Rocket algorithm.

    ROCKET (Marijan et al. 2013)
    """
    MAX_HISTORY_THRESHOLD = 10

    def __init__(self, all_test_results: Dict[int, Tuple[TestResult]]):
        """
        Rocket constructor.

        :param all_test_results: results of all tests
        """
        super().__init__()
        self.__all_test_results = all_test_results

    def predict(self) -> Iterable[int]:
        # Determine the maximal amount of historical results to consider.
        m = min(
            max(len(t) for t in self.__all_test_results.values()),
            Rocket.MAX_HISTORY_THRESHOLD
        )

        # Calculate the duration of the previous test execution.
        prev_duration = sum(
            t[0].duration for t in self.__all_test_results.values()
        )

        # Assign each test result with a successive id to allow storing them in
        # a matrix.
        test_ids = list(self.__all_test_results.keys())
        n = len(test_ids)

        # Create a failure matrix for all tests.
        failure_matrix = np.zeros((m, n))

        # Fill the failure matrix based on the failure status.
        for id, test in enumerate(test_ids):
            test_results = self.__all_test_results[test]
            test_results_len = len(test_results)
            for m_i in range(m):
                # Failsafe for tests that do not have sufficient executions,
                # assume the status is PASS.
                if m_i >= test_results_len:
                    failure_matrix[m_i, id] = 1
                else:
                    # Insert 1 if the test passed, else -1
                    test_passed = not test_results[m_i].failed
                    failure_matrix[m_i, id] = 1 if test_passed else -1

        # Calculate the cumulative priority for each test.
        def weight(distance):
            """
            Weight function to calculate the cumulative priority.

            :param distance: distance from the current test run
            :return: weight
            """
            if distance == 0:
                return 0.7
            elif distance == 1:
                return 0.2
            return 0.1

        cumulative_priority = (
            sum(failure_matrix[i, j] * weight(i) for i in range(m))
            for j in range(n)
        )

        # Add the test ids to the cumulative priority list.
        test_priorities = zip(test_ids, cumulative_priority)

        # Add the latest execution time to the priorities.
        adjusted_priorities = map(lambda p: (p[0], p[1] / prev_duration), map(
            lambda p: (p[0], p[1] + self.__all_test_results[p[0]][0].duration),
            test_priorities
        ))

        # Return the tests in order.
        return map(
            lambda p: p[0],
            sorted(adjusted_priorities, key=operator.itemgetter(1))
        )
