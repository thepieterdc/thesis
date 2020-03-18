# -*- coding: utf-8 -*-

"""Velocity predictors predictor."""
from abc import abstractmethod
from typing import Optional, List, Set, Iterable, Tuple, Dict

from src.entities.code_block import CodeBlock
from src.entities.repository import Repository
from src.entities.run import Run
from src.entities.test import Test

__author__ = "Pieter De Clercq"
__license__ = "MIT"


class AbstractDatabase:
    """
    Abstract database.
    """

    @abstractmethod
    def get_run_by_id(self, id: int) -> Optional[Run]:
        """
        Gets the given run.

        :param id: the id of the run to get
        :return: the run
        """
        return NotImplemented

    @abstractmethod
    def get_tests(self, repository: Repository) -> Dict[int, Set[CodeBlock]]:
        """
        Gets the tests in this repository.

        :param repository: the repository
        :return: tuples of the test id and a covered block. the same test be
                 returned multiple times, once for every covered block
        """
        return NotImplemented

    @abstractmethod
    def get_tests_by_coverage(self, run: Run, blocks: List[CodeBlock]) -> \
        Dict[Test, Set[CodeBlock]]:
        """
        Gets the tests that provide coverage for the given list of blocks.

        :param run: run, used to find the repository and base path
        :param blocks: list of code ranges
        :return: tests that cover the given code blocks
        """
        return NotImplemented

    @abstractmethod
    def update_run_set_order(self, run: Run, order: List[int]) -> None:
        """
        Saves the given predictors to the database.

        :param run: the corresponding run
        :param order: the predictors
        :return: nothing
        """
        return NotImplemented
