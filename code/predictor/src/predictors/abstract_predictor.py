# -*- coding: utf-8 -*-

"""Velocity predictors predictor."""

__author__ = "Pieter De Clercq"
__license__ = "MIT"

from abc import abstractmethod, ABCMeta
from typing import Iterable, Set

from entities import Test


class AbstractPredictor(metaclass=ABCMeta):
    """
    Abstract predictor.
    """

    def __init__(self, all_tests: Set[Test]):
        """
        AbstractPredictor constructor.

        :param all_tests: all tests that exist in the suite
        """
        self.__all_tests = all_tests

    @property
    def all_tests(self) -> Set[Test]:
        """
        Gets all tests in the suite

        :return: all tests
        """
        return set(self.__all_tests)

    @abstractmethod
    def predict(self) -> Iterable[int]:
        """
        Finds an order for the set of relevant tests.

        :return: the order
        """
        raise Exception("predict() is not implemented.")
