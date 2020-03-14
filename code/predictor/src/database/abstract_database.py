# -*- coding: utf-8 -*-

"""Velocity order predictor."""
from typing import Optional, List, Set

from src.entities.code_block import CodeBlock
from src.entities.run import Run

__author__ = "Pieter De Clercq"
__license__ = "MIT"


class AbstractDatabase:
    """
    Abstract database.
    """

    def get_tests_by_coverage(self, run: Run, blocks: List[CodeBlock]) -> \
        Set[CodeBlock]:
        """
        Gets the tests that provide coverage for the given list of blocks.

        :param run: run, used to find the repository and base path
        :param blocks: list of code ranges
        :return: tests that cover the given code blocks
        """
        raise Exception("get_tests_by_coverage() is not implemented.")

    def get_run_by_id(self, id: int) -> Optional[Run]:
        """
        Gets the given run.

        :param id: the id of the run to get
        :return: the run
        """
        raise Exception("get_run_by_id() is not implemented.")

    def update_run_set_order(self, run: Run, order: List[int]) -> None:
        """
        Saves the given order to the database.

        :param run: the corresponding run
        :param order: the order
        :return: nothing
        """
        raise Exception("update_run_set_order() is not implemented.")
