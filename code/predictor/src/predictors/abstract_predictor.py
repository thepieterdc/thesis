# -*- coding: utf-8 -*-

"""Velocity predictors predictor."""
from abc import abstractmethod, ABCMeta
from typing import Set, Tuple, List

from src.entities.code_block import CodeBlock
from src.entities.test import Test

__author__ = "Pieter De Clercq"
__license__ = "MIT"


class AbstractPredictor(metaclass=ABCMeta):
    """
    Abstract predictor.
    """

    def __init__(self):
        """
        AbstractPredictor constructor.
        """
        pass

    @abstractmethod
    def predict(self,
                all_tests: Set[int],
                relevant_tests: Set[Tuple[Test, CodeBlock]]) -> List[int]:
        """
        Finds an order for the set of relevant tests.

        :param all_tests: ids of all the tests in the repository
        :param relevant_tests: the tests that cover changed parts
        :return: the order
        """
        raise Exception("predict() is not implemented.")
