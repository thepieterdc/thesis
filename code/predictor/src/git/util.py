# -*- coding: utf-8 -*-

"""Velocity order predictor."""
import re
import sys

__author__ = "Pieter De Clercq"
__license__ = "MIT"

from typing import Tuple, List

match_regex = re.compile(r'@@ -(\d+),(\d+) ')


def parse_changes(diff: bytes):
    """
    Parses the changed lines from a diff.

    :param diff: the input diff
    :return: the changed lines
    """
    # Parse the diff to a string.
    diffstr = diff.decode(sys.getfilesystemencoding())

    # Iterate over the lines in the diff and match the ones that indicate the
    # start of a new chunk.
    for line in diffstr.splitlines():
        # Match the line with the regex.
        matches = match_regex.search(line)
        if matches:
            # Find the start position and the amount of lines.
            start, amount = tuple(map(int, map(matches.group, (1, 2))))
            # Yield the changed range.
            yield (start, start + amount - 1)
