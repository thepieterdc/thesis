/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */

#include <json.hpp>
#include <iostream>
#include <pqxx/transaction>
#include "manager.h"

using json = nlohmann::json;

#define PREPARED_TESTS_CREATE "tests_create"
#define PREPARED_TESTS_FIND_ID "tests_find_id"
#define PREPARED_TESTS_FIND_TESTCASE "tests_find_testcase"
#define PREPARED_TEST_RESULTS_CREATE "test_results_create"
#define PREPARED_TEST_RESULTS_FIND "test_results_find"

tests::manager::manager(pqxx::connection &db) : db(db) {
    this->db.prepare(PREPARED_TESTS_CREATE,
                     "INSERT INTO tests (repository_id, testcase) VALUES($1, $2) RETURNING id");
    this->db.prepare(PREPARED_TESTS_FIND_ID,
                     "SELECT testcase FROM tests WHERE id=$1 LIMIT 1");
    this->db.prepare(PREPARED_TESTS_FIND_TESTCASE,
                     "SELECT id FROM tests WHERE testcase=$1 AND repository_id=$2 LIMIT 1");
    this->db.prepare(PREPARED_TEST_RESULTS_CREATE,
                     "INSERT INTO tests_results (run_id, test_id, duration, failed) VALUES($1, $2, $3, $4)"
    );
    this->db.prepare(PREPARED_TEST_RESULTS_FIND,
                     "SELECT tr.failed,tr.id,tr.run_id,tr.test_id FROM tests_results tr INNER JOIN tests t ON (tr.test_id = t.id) WHERE t.testcase=$1 AND tr.run_id=$2 LIMIT 1"
    );
}

std::shared_ptr<tests::test>
tests::manager::create(const std::uint_fast64_t repository,
                       const std::string &testcase) const {
    // Start a transaction.
    pqxx::work tx(this->db);

    // Create a new test in the database.
    const auto result = tx.prepared(PREPARED_TESTS_CREATE)(repository)(testcase)
            .exec();

    // Commit the transaction.
    tx.commit();

    // Return the created test.
    return std::shared_ptr<tests::test>(new tests::test(
            result[0]["id"].as<std::uint_fast64_t>(),
            testcase)
    );
}

std::optional<std::shared_ptr<tests::test>>
tests::manager::find(const std::uint_fast64_t test_id) const {
    // Start a transaction.
    pqxx::work tx(this->db);

    // Attempt to find the test with the given id.
    const auto result = tx.prepared(PREPARED_TESTS_FIND_ID)(test_id).exec();

    // Commit the transaction.
    tx.commit();

    // Validate the result of the query.
    if (!result.empty()) {
        return std::make_optional(std::shared_ptr<tests::test>(new test(
                test_id,
                result[0]["testcase"].as<std::string>()
        )));
    }

    // Test was not found.
    return std::nullopt;
}

std::optional<std::shared_ptr<tests::test>>
tests::manager::find(const std::uint_fast64_t repository,
                     const std::string &testcase) const {
    // Start a transaction.
    pqxx::work tx(this->db);

    // Attempt to find the test with the given testcase name.
    const auto result = tx.prepared(PREPARED_TESTS_FIND_TESTCASE)
            (testcase)(repository).exec();

    // Commit the transaction.
    tx.commit();

    // Validate the result of the query.
    if (!result.empty()) {
        return std::make_optional(std::shared_ptr<tests::test>(new test(
                result[0]["id"].as<std::uint_fast64_t>(),
                testcase
        )));
    }

    // Test was not found.
    return std::nullopt;
}

std::optional<std::shared_ptr<tests::test_result>>
tests::manager::find_result(const std::uint_fast64_t run,
                            const std::string &testcase) const {
    // Start a transaction.
    pqxx::work tx(this->db);

    // Attempt to find the test with the given id.
    const auto result = tx.prepared(PREPARED_TEST_RESULTS_FIND)(testcase)(run)
            .exec();

    // Commit the transaction.
    tx.commit();

    // Validate the result of the query.
    if (!result.empty()) {
        return std::make_optional(std::shared_ptr<tests::test_result>(
                new test_result(
                        result[0][1].as<std::uint_fast64_t>(),
                        result[0][2].as<std::uint_fast64_t>(),
                        result[0][3].as<std::uint_fast64_t>(),
                        result[0][0].as<bool>())
        ));
    }

    // Test was not found.
    return std::nullopt;
}

std::size_t
tests::manager::parse_results(const runs::run &run, json results) const {
    // Iterate over the test results.
    for (json::iterator it = results.begin(); it != results.end(); ++it) {
        // Get the id of the test case.
        const auto opt_test = this->find(run.repository_id, it.key());
        const auto test = opt_test.has_value()
                          ? *opt_test
                          : this->create(run.repository_id, it.key());

        // Start a transaction.
        pqxx::work tx(this->db);
        const auto duration = it.value()["duration"].get<std::uint_fast64_t>();
        const auto result = it.value()["result"].get<bool>();

        // Insert the test result in the database.
        tx.prepared(PREPARED_TEST_RESULTS_CREATE)
                (run.id)(test->id)(duration)(!result).exec();

        // Commit the transaction.
        tx.commit();
    }

    // Return the amount of test results.
    return results.size();
}