# -*- coding: utf-8 -*-

"""Velocity predictors predictor."""

__author__ = "Pieter De Clercq"
__license__ = "MIT"

from abc import abstractmethod
from typing import Optional, List, Set, Tuple, Dict

from entities import CodeBlock, Repository, Run, Test, TestResult


class AbstractDatabase:
    """
    Abstract database.
    """

    @abstractmethod
    def create_prediction(self, run: Run, predictor_name: str, order: List[int],
                          predictor_selected: bool) -> None:
        """
        Creates a prediction in the database.

        :param run: the run
        :param predictor_name: the name of the predictor
        :param order: the predicted order
        :param predictor_selected: the selected predictor
        """
        raise NotImplemented

    @abstractmethod
    def get_predictions(self, run: Run) -> Tuple[Tuple[str, List[str]], ...]:
        """
        Gets the predicted result.

        :param run: the run
        :return: the predictions
        """
        raise NotImplemented

    @abstractmethod
    def get_preferred_predictor(self, repository: Repository) -> Optional[str]:
        """
        Gets the name of the preferred predictor.

        :param repository: the repository
        :return: the preferred predictor if any
        """
        raise NotImplemented

    @abstractmethod
    def get_run_by_id(self, id: int) -> Optional[Run]:
        """
        Gets the given run.

        :param id: the id of the run to get
        :return: the run
        """
        raise NotImplemented

    @abstractmethod
    def get_scores(self, repository: Repository) -> Tuple[Tuple[str, int], ...]:
        """
        Gets the predictor scores.

        :param repository: the repository
        :return: the predictor scores
        """
        raise NotImplemented

    @abstractmethod
    def get_tests(self, repository: Repository) -> Set[Test]:
        """
        Gets the tests in this repository.

        :param repository: the repository
        :return: tuples of the test id and a covered block. the same test be
                 returned multiple times, once for every covered block
        """
        raise NotImplemented

    @abstractmethod
    def get_tests_by_coverage(self, run: Run, blocks: List[CodeBlock]) -> \
        Set[Test]:
        """
        Gets the tests that provide coverage for the given list of blocks.

        :param run: run, used to find the repository and base path
        :param blocks: list of code ranges
        :return: tests that cover the given code blocks
        """
        raise NotImplemented

    @abstractmethod
    def get_test_by_id(self, id: int) -> Optional[str]:
        """
        Gets the given test.

        :param id: the id of the test to get
        :return: the test
        """
        raise NotImplemented

    @abstractmethod
    def get_test_results(self, repository: Repository) -> \
        Dict[int, Tuple[TestResult]]:
        """
        Gets the historical results of all tests in the repository, ordered by
        timestamp of execution (descending - latest result first).

        :param repository: the repository to find the tests for
        :return: the test results
        """
        raise NotImplemented

    @abstractmethod
    def get_unpredicted_run(self) -> Optional[Run]:
        """
        Gets the first unpredicted run.

        :return: the run if any
        """
        raise NotImplemented

    @abstractmethod
    def run_predicted(self, run: Run) -> None:
        """
        Marks the run as predicted.

        :param run: the run
        """
        raise NotImplemented
