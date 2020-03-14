/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */

#include <json.hpp>
#include <fstream>
#include <iostream>
#include "manager.h"

using json = nlohmann::json;

std::shared_ptr<tests::test>
tests::manager::create(const std::uint_fast64_t repository,
                       const std::string &testcase) const {
    // Create a new test in the database.
    const std::string sql(
            "INSERT INTO tests (repository_id, testcase) VALUES(?, ?)");
    const auto stmt = this->db.prepare(sql);
    stmt->bind_integer(1, repository);
    stmt->bind_text(2, testcase);
    const auto id = this->db.insert(*stmt);

    // Return the created test.
    return std::shared_ptr<tests::test>(new tests::test(id, testcase));
}

std::optional<std::shared_ptr<tests::test>>
tests::manager::find(const std::string &testcase) const {
    // Attempt to find the test with the given testcase name.
    const std::string sql("SELECT id FROM tests WHERE testcase=? LIMIT 1");
    const auto stmt = this->db.prepare(sql);
    stmt->bind_text(1, testcase);
    const auto found = this->db.find(*stmt);

    // Validate the result of the query.
    if (found) {
        return std::make_optional(std::shared_ptr<tests::test>(
                new test(stmt->get_integer(0), testcase)
        ));
    }

    // Test was not found.
    return std::nullopt;
}

std::optional<std::shared_ptr<tests::test>>
tests::manager::find(const std::uint_fast64_t test_id) const {
    // Attempt to find the test with the given id.
    const std::string sql("SELECT testcase FROM tests WHERE id=? LIMIT 1");
    const auto stmt = this->db.prepare(sql);
    stmt->bind_integer(1, test_id);
    const auto found = this->db.find(*stmt);

    // Validate the result of the query.
    if (found) {
        return std::make_optional(std::shared_ptr<tests::test>(
                new test(test_id, stmt->get_text(0))
        ));
    }

    // Test was not found.
    return std::nullopt;
}

std::optional<std::shared_ptr<tests::test_result>>
tests::manager::find_result(const std::uint_fast64_t run,
                            const std::string &testcase) const {
    // Attempt to find the test with the given id.
    const std::string sql(
            "SELECT tr.failed,tr.id,tr.run_id,tr.test_id FROM tests_results tr INNER JOIN tests t ON (tr.test_id = t.id) WHERE t.testcase=? AND tr.run_id=? LIMIT 1"
    );
    const auto stmt = this->db.prepare(sql);
    stmt->bind_text(1, testcase);
    stmt->bind_integer(2, run);
    const auto found = this->db.find(*stmt);

    // Validate the result of the query.
    if (found) {
        return std::make_optional(std::shared_ptr<tests::test_result>(
                new test_result(stmt->get_integer(1), stmt->get_integer(2),
                                stmt->get_integer(3), stmt->get_boolean(0))
        ));
    }

    // Test was not found.
    return std::nullopt;
}

std::size_t
tests::manager::parse(const runs::run &run, json results) const {
    // Iterate over the test results.
    for (json::iterator it = results.begin(); it != results.end(); ++it) {
        // Get the id of the test case.
        const auto opt_test = this->find(it.key());
        const auto test = opt_test.has_value()
                          ? *opt_test
                          : this->create(run.repository_id, it.key());

        // Insert the test result in the database.
        const std::string sql(
                "INSERT INTO tests_results (run_id, test_id, failed) VALUES(?, ?, ?)"
        );
        const auto stmt = this->db.prepare(sql);
        stmt->bind_integer(1, run.id);
        stmt->bind_integer(2, test->id);
        stmt->bind_boolean(3, !it.value());
        this->db.insert(*stmt);
    }

    // Return the amount of test results.
    return results.size();
}