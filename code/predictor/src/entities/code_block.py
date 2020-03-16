# -*- coding: utf-8 -*-

"""Velocity predictors predictor."""

__author__ = "Pieter De Clercq"
__license__ = "MIT"


class CodeBlock:
    """
    A block of code in a file.
    """

    def __init__(self, file: str, from_line: int, to_line: int):
        """
        CodeBlock constructor.

        :param file: name of the source file
        :param from_line: start line of the block
        :param to_line: end line of the block
        """
        self.__file = file
        self.__from_line = from_line
        self.__to_line = to_line

    @property
    def file(self) -> str:
        """
        file accessor.

        :return: the file
        """
        return self.__file

    @property
    def from_line(self) -> int:
        """
        from_line accessor.

        :return: the start line of the block
        """
        return self.__from_line

    def __str__(self):
        return f"CodeBlock({self.__file}, {self.__from_line} - {self.__to_line})"

    @property
    def to_line(self) -> int:
        """
        to_line accessor.

        :return: the end line of the block
        """
        return self.__to_line
