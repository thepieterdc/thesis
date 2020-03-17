# -*- coding: utf-8 -*-

"""Velocity predictors predictor."""

__author__ = "Pieter De Clercq"
__license__ = "MIT"


class CodeLine:
    """
    A line of code in a file.
    """

    def __init__(self, file: str, line: int):
        """
        CodeLine constructor.

        :param file: name of the source file
        :param line: line of the code
        """
        self.__file = file
        self.__line = line

    def __eq__(self, other):
        if isinstance(other, CodeLine):
            return self.__file == other.__file and self.__line == other.__line
        return NotImplemented

    @property
    def file(self) -> str:
        """
        file accessor.

        :return: the file
        """
        return self.__file

    def __hash__(self):
        return hash(self.__repr__())

    @property
    def line(self) -> int:
        """
        line accessor.

        :return: the line  number
        """
        return self.__line

    def __repr__(self):
        return f"{self.__file}:{self.__line}"

    def __str__(self):
        return f"CodeLine({self.__file}:{self.__line})"
