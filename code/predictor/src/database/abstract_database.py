# -*- coding: utf-8 -*-

"""Velocity predictors predictor."""
from abc import abstractmethod
from typing import Optional, List, Set, Iterable, Tuple

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
        raise Exception("get_run_by_id() is not implemented.")

    @abstractmethod
    def get_test_ids(self, repository: Repository) -> Iterable[int]:
        """
        Gets the ids of the tests in this repository.

        :param repository: the repository
        :return: the test ids
        """
        raise Exception("get_test_ids() is not implemented.")

    @abstractmethod
    def get_tests_by_coverage(self, run: Run, blocks: List[CodeBlock]) -> \
        Iterable[Tuple[Test, CodeBlock]]:
        """
        Gets the tests that provide coverage for the given list of blocks.

        :param run: run, used to find the repository and base path
        :param blocks: list of code ranges
        :return: tests that cover the given code blocks
        """
        raise Exception("get_tests_by_coverage() is not implemented.")

    @abstractmethod
    def update_run_set_order(self, run: Run, order: List[int]) -> None:
        """
        Saves the given predictors to the database.

        :param run: the corresponding run
        :param order: the predictors
        :return: nothing
        """
        raise Exception("update_run_set_order() is not implemented.")
