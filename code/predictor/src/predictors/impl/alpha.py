# -*- coding: utf-8 -*-

"""Velocity predictors predictor."""

__author__ = "Pieter De Clercq"
__license__ = "MIT"

from functools import reduce
from typing import Set, Tuple, Dict, Generator

from entities import Test, TestResult
from predictors.abstract_predictor import AbstractPredictor


class Alpha(AbstractPredictor):
    """
    Predictor that ranks tests using the Alpha algorithm as described in my
    paper.
    """

    def __init__(self, all_tests: Set[Test], affected_tests: Set[Test],
                 test_results: Dict[int, Tuple[TestResult]]):
        """
        Alpha constructor.

        :param all_tests: all the tests
        :param affected_tests: the tests that cover changed parts of the code
        :param test_results: results of every test
        """
        super().__init__(all_tests)
        self.__affected_tests = affected_tests
        self.__test_results = test_results

    def __average_duration(self, test: Test) -> int:
        """
        Calculates the average test duration in nanoseconds.

        :param test: the average test duration
        :return: the average duration
        """
        # Find whether this test has ever been successful.
        if any(not t.failed for t in self.__test_results[test.id]):
            candidates = filter(
                lambda t: not t.failed,
                self.__test_results[test.id]
            )
        else:
            candidates = self.__test_results[test.id]

        # Find the average duration over all executions.
        total_duration = reduce(
            lambda acc, r: (acc[0] + r.duration, acc[1] + 1),
            candidates,
            (0, 0)
        )

        return total_duration[0] / total_duration[1]

    def __failing_tests(self) -> Generator[int, None, None]:
        """
        Finds the tests that have failed in the last 3 runs.

        :return: the ids of the failing tests
        """
        for test, results in self.__test_results.items():
            if any(res.failed for res in results[:3]):
                yield test

    def predict(self) -> Generator[int, None, None]:
        # Store the average duration per test.
        test_durations = {
            t.id: self.__average_duration(t) for t in self.all_tests
        }

        # Create a map of the tests to their coverage lines.
        tests_lines = {
            test.id: set(line for line in cov)
            for test in self.all_tests for cov in test.coverage
        }

        # Store the ids of the tests.
        affected_test_ids = set(t.id for t in self.__affected_tests)
        all_test_ids = set(t.id for t in self.all_tests)
        failing_test_ids = set(self.__failing_tests())

        # Execute all the failing affected tests, sorted by their duration.
        failed_affecting_tests = sorted(
            affected_test_ids & failing_test_ids,
            key=lambda t: test_durations[t]
        )
        for test in failed_affecting_tests:
            yield test

            # Remove the now-covered lines from the test lines set.
            covered_lines = tests_lines[test]
            for t in tests_lines.keys():
                tests_lines[t] -= covered_lines

            # Remove them from the candidates.
            del tests_lines[test]
            affected_test_ids -= {test}
            all_test_ids -= {test}
            failing_test_ids -= {test}

        # Execute all the failing tests, sorted by their duration.
        for test in sorted(failing_test_ids, key=lambda t: test_durations[t]):
            yield test

            # Remove the now-covered lines from the test lines set.
            covered_lines = tests_lines[test]
            for t in tests_lines.keys():
                tests_lines[t] -= covered_lines

            # Remove them from the candidates.
            del tests_lines[test]
            affected_test_ids -= {test}
            all_test_ids -= {test}

        # Execute the affected tests, sorted by their coverage.
        while affected_test_ids:
            # Find the test that adds the most uncovered lines. This needs to be
            # computed twice to guarantee a deterministic order.
            max_cov_amt = max(
                len(v) for k, v in tests_lines.items()
                if k in affected_test_ids
            )
            max_test, max_cov = max(
                i for i in tests_lines.items()
                if len(i[1]) == max_cov_amt and i[0] in affected_test_ids,
            )

            # Return the test.
            yield max_test
            del tests_lines[max_test]
            affected_test_ids -= {max_test}
            all_test_ids -= {max_test}

            # Mark the lines in the cover set of the test as covered.
            for test in tests_lines.keys():
                tests_lines[test] -= max_cov

        # Remove all tests from the test lines that no longer contribute any
        # coverage.
        tests_lines = {t: v for t, v in tests_lines.items() if v}

        # Execute the remaining tests, sorted by their coverage.
        while tests_lines:
            # Find the test that adds the most uncovered lines. This needs to be
            # computed twice to guarantee a deterministic order.
            max_cov_amt = max(
                len(v) for k, v in tests_lines.items()
            )
            max_test, max_cov = max(
                i for i in tests_lines.items() if len(i[1]) == max_cov_amt,
            )

            # Return the test.
            yield max_test
            del tests_lines[max_test]
            all_test_ids -= {max_test}

            # Mark the lines in the cover set of the test as covered.
            for test in tests_lines.keys():
                tests_lines[test] -= max_cov

        # Execute all remaining tests that will not contribute anything.
        for t in all_test_ids:
            yield t
