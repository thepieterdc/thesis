# -*- coding: utf-8 -*-

"""Velocity predictors predictor."""
from typing import Optional, List, Tuple, Iterable, Generator

import psycopg2

from database.abstract_database import AbstractDatabase
from entities import CodeBlock
from entities import Repository
from entities import Run
from entities import Test

__author__ = "Pieter De Clercq"
__license__ = "MIT"


class PostgresDatabase(AbstractDatabase):
    """
    PostgreSQL database adapter.
    """

    def __init__(self, conn_str: str):
        """
        SQLiteDatabase constructor.

        :param conn_str: connection string
        """
        self.__connection = psycopg2.connect(conn_str)

    def get_run_by_id(self, id: int) -> Optional[Run]:
        cursor = self.__connection.cursor()
        cursor.execute(
            "SELECT id, repository_id, commit_hash FROM runs WHERE id=%s",
            (id,))
        run_result = cursor.fetchone()

        if run_result:
            cursor.execute(
                "SELECT id, url FROM repositories WHERE id=%s",
                (run_result[1],))

            # Return the found run.
            repository = Repository(*cursor.fetchone())
            cursor.close()
            return Run.from_cursor(run_result, repository)

        cursor.close()

        # Run not found.
        return None

    def get_tests(self, repository: Repository) -> \
        Generator[Tuple[int, CodeBlock], None, None]:
        cursor = self.__connection.cursor()
        cursor.execute(
            "SELECT test_id, sourcefile, from_line, to_line FROM tests_coverage"
        )

        # Iterate over every test.
        for row in cursor.fetchall():
            yield (row[0], CodeBlock(row[1], row[2], row[3]))

    def get_test_ids(self, repository: Repository) -> \
        Generator[int, None, None]:
        cursor = self.__connection.cursor()
        cursor.execute("SELECT id FROM tests WHERE repository_id=%s",
                       (repository.id,))

        # Iterate over every test.
        for row in cursor.fetchall():
            yield row[0]
        cursor.close()

    def get_tests_by_coverage(self, run: Run, blocks: List[CodeBlock]) -> \
        Generator[Tuple[Test, CodeBlock], None, None]:
        cursor = self.__connection.cursor()

        # Iterate over every block.
        for block in blocks:
            # Find all tests that cover this block.
            cursor.execute(
                "SELECT t.id,tc.from_line,tc.to_line FROM tests_coverage tc "
                "INNER JOIN tests t on tc.test_id = t.id WHERE "
                "t.repository_id=%s AND tc.sourcefile=%s AND tc.from_line <= "
                "%s AND %s <= tc.to_line",
                (run.repository.id, block.file, block.to_line, block.from_line))

            # Add the coverage
            for row in cursor.fetchall():
                yield (
                    Test(row[0], CodeBlock(block.file, row[1], row[2])),
                    block
                )

        cursor.close()

    def update_run_set_order(self, run: Run, order: List[int]) -> None:
        cursor = self.__connection.cursor()
        cursor.execute("UPDATE runs SET testorder = %s WHERE id=%s",
                       (",".join(map(str, order)), run.id))
        self.__connection.commit()
        cursor.close()
