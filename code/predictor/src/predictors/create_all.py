# -*- coding: utf-8 -*-

"""Velocity predictors predictor."""

__author__ = "Pieter De Clercq"
__license__ = "MIT"

from typing import Tuple, Set, Dict, Iterable

from entities import Test, TestResult, CodeBlock
from predictors.abstract_predictor import AbstractPredictor
from predictors.impl.affected_random import AffectedRandom
from predictors.impl.all_in_order import AllInOrder
from predictors.impl.all_random import AllRandom
from predictors.impl.alpha import Alpha
from predictors.impl.greedy_cover_affected import GreedyCoverAffected
from predictors.impl.greedy_cover_all import GreedyCoverAll
from predictors.impl.greedy_time_all import GreedyTimeAll
from predictors.impl.hgs_affected import HGSAffected
from predictors.impl.hgs_all import HGSAll
from predictors.impl.rocket import Rocket


def create_all_predictors(all_tests: Set[Test], affected_tests: Set[Test],
                          all_test_results: Dict[int, Tuple[TestResult]],
                          affected_code: Iterable[CodeBlock]) \
    -> Set[AbstractPredictor]:
    """
    Creates a set of instances of all the predictors.

    :param all_tests: all tests
    :param affected_tests: all affected tests
    :param all_test_results: the results of all tests
    :param affected_code: the affected code blocks
    :return: instances of all predictors
    """
    return {
        AffectedRandom(all_tests, affected_tests),
        AllInOrder(all_tests),
        AllRandom(all_tests),
        Alpha(all_tests, affected_tests, all_test_results),
        GreedyCoverAffected(affected_code, all_tests),
        GreedyCoverAll(all_tests),
        GreedyTimeAll(all_tests, all_test_results),
        HGSAffected(all_tests, affected_tests),
        HGSAll(all_tests),
        Rocket(all_tests, all_test_results)
    }
