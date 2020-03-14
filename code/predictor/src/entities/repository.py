# -*- coding: utf-8 -*-

"""Velocity order predictor."""

__author__ = "Pieter De Clercq"
__license__ = "MIT"

import logging
import tempfile
from typing import Iterable

import git

from src.entities.code_block import CodeBlock
from src.git.clone_progress_logger import CloneProgressLogger
from src.git.util import parse_changes


class Repository:
    """
    A git repository.
    """

    def __init__(self, id: int, repository_url: str):
        """
        Repository constructor.

        :param id: id of the repository
        :param repository_url: url to the repository
        """
        self.__id = id
        self.__url = repository_url

    def changes(self, commit_hash: str) -> Iterable[CodeBlock]:
        """
        Fetches the changes in the given commit.

        :param commit_hash: the hash of the commit to analyse
        :return: the changes
        """
        with tempfile.TemporaryDirectory() as repodir:
            # Clone the repository.
            logging.info('Cloning the repository...')
            repo = git.Repo.clone_from(self.__url, repodir,
                                       progress=CloneProgressLogger())

            # Checkout the required commit.
            logging.info('Finding commit...')
            commit = repo.commit(commit_hash)
            message = commit.message.replace("\n", "\\n")
            logging.info(f'Checked out #{commit.hexsha[:7]} - {message}')

            # Get the changes.
            logging.info('Parsing changed files...')
            changes = commit.diff(commit.parents[0], create_patch=True)
            amt_changes = len(changes)
            for idx, item in enumerate(changes):
                file_name = item.a_path
                diff = parse_changes(item.diff)
                logging.info(f'[{idx + 1}/{amt_changes}] Parsed {file_name}.')

                for change in diff:
                    start, end = change
                    yield CodeBlock(file_name, start, end)

    @property
    def id(self) -> int:
        """
        id accessor.

        :return: the id
        """
        return self.__id

    def __str__(self):
        return f"Repository({self.__url})"

    @property
    def url(self) -> str:
        """
        url accessor.

        :return: the url
        """
        return self.__url
