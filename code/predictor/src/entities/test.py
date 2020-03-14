# -*- coding: utf-8 -*-

"""Velocity order predictor."""
from src.entities.code_block import CodeBlock

__author__ = "Pieter De Clercq"
__license__ = "MIT"

from src.entities.repository import Repository


class Test:
    """
    A test.
    """

    def __init__(self, id: int, coverage: CodeBlock):
        """
        Test constructor.

        :param id: run id
        :param coverage: block of code that is covered by this test
        """
        self.__coverage = coverage
        self.__id = id

    @property
    def coverage(self) -> CodeBlock:
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
        return f"Test({self.__id}, {self.__coverage})"
