# -*- coding: utf-8 -*-

"""Velocity predictors predictor."""

__author__ = "Pieter De Clercq"
__license__ = "MIT"

from abc import abstractmethod, ABCMeta
from typing import Iterable


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
    def predict(self) -> Iterable[int]:
        """
        Finds an order for the set of relevant tests.

        :return: the order
        """
        raise Exception("predict() is not implemented.")
