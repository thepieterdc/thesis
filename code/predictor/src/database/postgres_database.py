# -*- coding: utf-8 -*-

"""Velocity predictors predictor."""
from collections import defaultdict
from typing import Optional, List, Tuple, Iterable, Generator, Dict, Set

import psycopg2

from database.abstract_database import AbstractDatabase
from entities import CodeBlock, TestResult
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

    def create_prediction(self, run: Run, predictor_name: str, order: List[int],
                          predictor_selected: bool) -> None:
        # Find the predictor.
        predictor = self.__get_predictor(predictor_name)
        if not predictor:
            predictor = self.__create_predictor(predictor_name)

        # Parse the order to a string.
        order_str = ",".join(map(str, order))

        # Insert the prediction into the database.
        cursor = self.__connection.cursor()
        cursor.execute(
            "INSERT INTO predictions (run_id, predictor_id, testorder, selected) VALUES (%s, %s, %s, %s)",
            (run.id, predictor, order_str, predictor_selected))
        self.__connection.commit()

        # Close the connection.
        cursor.close()

    def __create_predictor(self, name: str) -> Optional[int]:
        """
        Creates a predictor with the given name.

        :param name: the name
        :return: the id of the created predictor
        """
        cursor = self.__connection.cursor()
        cursor.execute("INSERT INTO predictors (name) VALUES (%s) RETURNING id",
                       (name,))
        self.__connection.commit()
        create_result = cursor.fetchone()

        # Close the connection.
        cursor.close()

        return create_result[0]

    def __get_predictor(self, name: str) -> Optional[int]:
        """
        Gets the id of the predictor with the given name.

        :param name: the name
        :return: the id of the predictor if it exists
        """
        cursor = self.__connection.cursor()
        cursor.execute("SELECT id FROM predictors WHERE name=%s", (name,))
        predictor_result = cursor.fetchone()

        # Close the connection.
        cursor.close()

        return None if not predictor_result else predictor_result[0]

    def get_predictions(self, run: Run) -> Tuple[Tuple[str, List[str]], ...]:
        # Get the test names.
        tcursor = self.__connection.cursor()
        tcursor.execute(
            "SELECT t.id, t.testcase FROM tests t WHERE t.repository_id=%s",
            (run.repository.id,))
        test_cases = {int(t[0]): t[1] for t in tcursor.fetchall()}
        tcursor.close()

        # Get the predictions.
        cursor = self.__connection.cursor()

        cursor.execute(
            "SELECT p.name, pr.testorder FROM predictions pr INNER JOIN predictors p on pr.predictor_id = p.id WHERE run_id=%s",
            (run.id,))

        for resp in cursor.fetchall():
            name, testorder = resp
            if not testorder:
                yield name, list()
            else:
                orders = list(
                    map(lambda d: test_cases[int(d)], testorder.split(",")))

                yield name, orders

        # Close the connection.
        cursor.close()

    def get_preferred_predictor(self, repository: Repository) -> Optional[str]:
        cursor = self.__connection.cursor()
        cursor.execute(
            "SELECT p.name FROM predictors_scores ps INNER JOIN predictors p ON ps.predictor_id = p.id WHERE repository_id=%s ORDER BY score DESC LIMIT 1",
            (repository.id,))
        result = cursor.fetchone()

        # Close the connection.
        cursor.close()

        return None if not result else result[0]

    def get_repository(self, url: str) -> Optional[Repository]:
        cursor = self.__connection.cursor()
        cursor.execute("SELECT id FROM repositories WHERE url=%s", (url,))
        repository_result = cursor.fetchone()

        if repository_result:
            repository = Repository(repository_result[0], url)
            cursor.close()
            return repository

        cursor.close()

        # Repository not found.
        return None

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

    def get_scores(self, repository: Repository) -> Tuple[Tuple[str, int], ...]:
        cursor = self.__connection.cursor()
        cursor.execute(
            "SELECT p.name, ps.score FROM predictors_scores ps INNER JOIN predictors p on ps.predictor_id = p.id WHERE ps.repository_id=%s",
            (repository.id,)
        )

        yield from cursor.fetchall()

        # Close the connection.
        cursor.close()

    def get_tests(self, repository: Repository) -> Set[Test]:
        cursor = self.__connection.cursor()
        cursor.execute(
            "SELECT test_id, sourcefile, from_line, to_line FROM tests_coverage tc INNER JOIN tests t on tc.test_id = t.id WHERE t.repository_id=%s",
            (repository.id,)
        )

        # Iterate over every test.
        ret = defaultdict(set)
        for row in cursor.fetchall():
            ret[row[0]].add(CodeBlock(row[1], row[2], row[3]))
        cursor.close()

        # Iterate over the results.
        return set(Test(id, blocks) for id, blocks in ret.items())

    def get_tests_by_coverage(self, repository: Repository,
                              blocks: List[CodeBlock]) -> Set[Test]:
        cursor = self.__connection.cursor()

        ret = defaultdict(set)

        # Iterate over every block.
        for b in blocks:
            # Find all tests that cover this block.
            cursor.execute(
                "SELECT t.id,tc.from_line,tc.to_line FROM tests_coverage tc "
                "INNER JOIN tests t on tc.test_id = t.id WHERE "
                "t.repository_id=%s AND tc.sourcefile=%s AND tc.from_line <= "
                "%s AND %s <= tc.to_line",
                (repository.id, b.file, b.to_line, b.from_line))

            # Add the coverage
            for row in cursor.fetchall():
                ret[row[0]].add(CodeBlock(b.file, row[1], row[2]))

        cursor.close()

        # Iterate over the results.
        return set(Test(id, blocks) for id, blocks in ret.items())

    def get_test_by_id(self, id: int) -> Optional[str]:
        cursor = self.__connection.cursor()
        cursor.execute(
            "SELECT testcase FROM tests WHERE id=%s",
            (id,))
        test_result = cursor.fetchone()

        if test_result:
            return test_result[0]

        # Test not found.
        return None

    def get_test_results(self, repository: Repository) -> \
        Dict[int, Tuple[TestResult]]:
        cursor = self.__connection.cursor()
        cursor.execute(
            "SELECT t.id, tr.failed, tr.duration FROM tests t INNER JOIN tests_results tr on t.id = tr.test_id WHERE t.repository_id=%s ORDER BY tr.id DESC",
            (repository.id,))

        # Iterate over every test.
        ret = defaultdict(list)
        for row in cursor.fetchall():
            ret[row[0]].append(TestResult(row[2], row[1]))

        # Return the result.
        cursor.close()
        return {test: tuple(results) for test, results in ret.items()}

    def get_unpredicted_run(self) -> Optional[Run]:
        cursor = self.__connection.cursor()
        cursor.execute(
            "SELECT id, repository_id, commit_hash FROM runs WHERE predicted=false"
        )
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

        # No run was found.
        return None

    def run_predicted(self, run: Run) -> None:
        cursor = self.__connection.cursor()
        cursor.execute("UPDATE runs SET predicted=true WHERE id=%s",
                       (run.id,))
        self.__connection.commit()

        # Close the connection.
        cursor.close()
