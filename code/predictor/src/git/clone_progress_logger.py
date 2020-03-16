# -*- coding: utf-8 -*-

"""Velocity predictors predictor."""

__author__ = "Pieter De Clercq"
__license__ = "MIT"

import logging
from git import RemoteProgress


class CloneProgressLogger(RemoteProgress):
    """
    Logs the clone progress using the logger.
    """

    def update(self, op_code, cur_count, max_count=None, message='') -> None:
        if message:
            logging.debug(message)
