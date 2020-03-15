/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */

#include <iostream>
#include <fstream>
#include <pqxx/transaction>
#include "manager.h"

#define PREPARED_COVERAGE_AVAILABLE "coverage_available"
#define PREPARED_COVERAGE_CREATE "coverage_create"
#define PREPARED_COVERAGE_DELETE "coverage_delete"

coverage::manager::manager(pqxx::connection &db, const tests::manager &tests) :
        db(db), tests(tests) {
    this->db.prepare(PREPARED_COVERAGE_AVAILABLE,
                     "SELECT COUNT(1) FROM tests_coverage WHERE test_id=$1"
    );
    this->db.prepare(PREPARED_COVERAGE_CREATE,
                     "INSERT INTO tests_coverage (test_id, sourcefile, from_line, to_line) VALUES($1, $2, $3, $4)"
    );
    this->db.prepare(PREPARED_COVERAGE_DELETE,
                     "DELETE FROM tests_coverage WHERE test_id=$1");
}

bool coverage::manager::available(const std::uint_fast64_t test_id) const {
    // Start a transaction.
    pqxx::work tx(this->db);

    const auto result = tx.prepared(PREPARED_COVERAGE_AVAILABLE)(test_id)
            .exec();

    // Commit the transaction.
    tx.commit();

    // Validate the result of the query.
    return result[0][0].as<std::uint_fast64_t>() > 0;
}

void coverage::manager::clear(const std::uint_fast64_t test_id) const {
    // Start a transaction.
    pqxx::work tx(this->db);

    // Remove the coverage data.
    tx.prepared(PREPARED_COVERAGE_DELETE)(test_id).exec();

    // Commit the transaction.
    tx.commit();
}

std::size_t coverage::manager::parse(std::uint_fast64_t run, json data) const {
    size_t processed = 0;
    // Iterate over the coverage data.
    for (auto &file : data) {
        // Get the test case.
        const auto test_case = file["test"].get<std::string>();

        // Get the result of the test case in this run.
        const auto test_result = this->tests.find_result(run, test_case);
        if (!test_result.has_value()) {
            throw std::runtime_error("Test result not found.");
        }

        // Find whether the coverage for this test should be saved.
        const auto test_id = (*test_result)->test_id;
        if (this->available(test_id) && (*test_result)->failed) {
            // Coverage for this test is already available, however the test did
            // not reach the end, so the updated coverage may possibly not
            // represent the actual test coverage.
            continue;
        }

        // Delete the current test coverage information for this test.
        this->clear(test_id);

        // Iterate over the coverage items.
        auto lines = file["lines"];
        for (auto &line : lines) {
            // Start a transaction.
            pqxx::work tx(this->db);

            // Insert the data into the database.
            const auto file_name = line["file"].get<std::string>();
            const auto from = line["from"].get<std::uint_fast32_t>();
            const auto to = line["to"].get<std::uint_fast32_t>();
            tx.prepared(PREPARED_COVERAGE_CREATE)(test_id)(file_name)(from)
                    (to).exec();

            // Commit the transaction.
            tx.commit();
        }

        processed++;
    }

    return processed;
}