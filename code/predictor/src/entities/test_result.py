# -*- coding: utf-8 -*-

"""Velocity predictors predictor."""

__author__ = "Pieter De Clercq"
__license__ = "MIT"

from typing import Set

from entities import CodeBlock


class TestResult:
    """
    The result of a test.
    """

    def __init__(self, duration: int, failed: bool):
        """
        TestResult constructor.

        :param duration: the test duration in nanoseconds
        :param failed: true if the test failed
        """
        self.__duration = duration
        self.__failed = failed

    @property
    def duration(self) -> int:
        """
        duration accessor.

        :return: the duration in nanoseconds
        """
        return self.__duration

    @property
    def failed(self) -> int:
        """
        failure accessor.

        :return: true if the test failed
        """
        return self.__failed

    def __repr__(self):
        return f"{'FAIL' if self.__failed else 'PASS'} - {self.__duration}ns"

    def __str__(self):
        return f"TestResult({'FAIL' if self.__failed else 'PASS'} - {self.__duration}ns)"
