# -*- coding: utf-8 -*-

"""Velocity predictors predictor."""

__author__ = "Pieter De Clercq"
__license__ = "MIT"

from typing import Set

from entities import CodeBlock


class Test:
    """
    A test.
    """

    def __init__(self, id: int, coverage: Set[CodeBlock]):
        """
        Test constructor.

        :param id: run id
        :param coverage: blocks of code that are covered by this test
        """
        self.__coverage = coverage
        self.__id = id

    @property
    def coverage(self) -> Set[CodeBlock]:
        """
        coverage accessor.

        :return: the coverage
        """
        return self.__coverage

    @property
    def id(self) -> int:
        """
        id accessor.

        :return: the id
        """
        return self.__id

    def __str__(self):
        return f"Test({self.__id})"
