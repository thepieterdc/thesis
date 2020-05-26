# -*- coding: utf-8 -*-

"""Velocity CLI command."""

__author__ = "Pieter De Clercq"
__license__ = "MIT"

from abc import abstractmethod, ABCMeta
from typing import Iterable

from database.abstract_database import AbstractDatabase


class AbstractCommand(metaclass=ABCMeta):
    """
    Abstract command.
    """

    def __init__(self, db: AbstractDatabase):
        self._db = db

    @abstractmethod
    def run(self, arguments: Iterable[str]) -> None:
        """
        Executes the command.

        :param arguments: command line arguments
        :return: the order
        """
        raise Exception("predict() is not implemented.")
