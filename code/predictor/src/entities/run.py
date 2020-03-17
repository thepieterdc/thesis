# -*- coding: utf-8 -*-

"""Velocity predictors predictor."""

__author__ = "Pieter De Clercq"
__license__ = "MIT"

from entities import Repository


class Run:
    """
    A run.
    """

    def __init__(self, id: int, commit: str, repository: Repository):
        """
        Run constructor.

        :param id: run id
        :param commit: commit hash
        :param repository: the repository
        """
        self.__commit = commit
        self.__id = id
        self.__repository = repository

    @property
    def commit(self) -> str:
        """
        commit accessor.

        :return: the commit
        """
        return self.__commit

    @staticmethod
    def from_cursor(run_cursor: tuple, repository: Repository) -> 'Run':
        """
        Creates a new Run object from the given cursor and repository.

        :param run_cursor: run cursor
        :param repository: clone repository
        :return: run instance
        """
        return Run(run_cursor[0], run_cursor[2], repository)

    @property
    def id(self) -> int:
        """
        id accessor.

        :return: the id
        """
        return self.__id

    @property
    def repository(self) -> Repository:
        """
        repository accessor.

        :return: the repository
        """
        return self.__repository

    def __str__(self):
        return f"Run({self.__id}, '{self.__commit}' @ {self.__repository})"
