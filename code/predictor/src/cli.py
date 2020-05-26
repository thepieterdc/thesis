#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Velocity predictors predictor."""

__author__ = "Pieter De Clercq"
__license__ = "MIT"

import logging
import sys

from commands import *
from database import PostgresDatabase

# Set-up the logger.
logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S',
                    level=logging.INFO)

# Commands.
commands = {Affected, Durations, Failures, Predict, Predictions, Scores}


def usage():
    """
    Prints the usage instructions.
    """
    logging.error(f'Syntax: {sys.argv[0]} database_string command')
    logging.error(
        f"Available commands: [{', '.join(str(c.name()) for c in commands)}]")
    exit(1)


# Input validation.
if len(sys.argv) < 3:
    usage()

# Create a database connection.
db = PostgresDatabase(sys.argv[1])
logging.info("Connected to the database.")

# Parse the command.
command = sys.argv[2]

command_cls = None
try:
    command_cls = next(comm for comm in commands if comm.name() == command)
except StopIteration:
    usage()

command_cls(db).run(sys.argv[3:])
