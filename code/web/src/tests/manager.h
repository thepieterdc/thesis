/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */

#ifndef WEB_TESTS_MANAGER_H
#define WEB_TESTS_MANAGER_H

#include <json.hpp>
#include "../database/connection.h"
#include "../runs/run.h"
#include "test.h"
#include "test_result.h"

using json = nlohmann::json;

namespace tests {
    using test_results =
    std::map<std::uint_fast64_t, std::shared_ptr<tests::test_result>>;

    /**
     * Manages tests.
     */
    class manager {
    private:
        pqxx::connection &db;

        /**
         * Creates a new test.
         *
         * @param repository id of the repository
         * @param testcase the name of the testcase
         * @return the created test
         */
        [[nodiscard]] std::shared_ptr<tests::test>
        create(std::uint_fast64_t repository,
               const std::string &testcase) const;

    public:
        /**
         * manager constructor.
         *
         * @param db database connection
         */
        explicit manager(pqxx::connection &db);

        /**
         * manager destructor.
         */
        virtual ~manager() = default;

        /**
         * Finds a test by its id.
         *
         * @param id the id of the testcase
         * @return the test if found
         */
        [[nodiscard]] std::optional<std::shared_ptr<tests::test>>
        find(std::uint_fast64_t id) const;

        /**
         * Finds a test by the name of the testcase.
         *
         * @param repository the id of the repository
         * @param testcase the name of the testcase
         * @return the test if found
         */
        [[nodiscard]] std::optional<std::shared_ptr<tests::test>>
        find(std::uint_fast64_t repository, const std::string &testcase) const;

        /**
         * Finds all test results of the given run.
         *
         * @param run the run
         * @return the test results
         */
        [[nodiscard]] test_results find_results(std::uint_fast64_t run) const;

        /**
         * Finds a test result by the name of the testcase.
         *
         * @param run the id of the run
         * @param testcase the name of the testcase
         * @return the test result if found
         */
        [[nodiscard]] std::optional<std::shared_ptr<tests::test_result>>
        find_result(std::uint_fast64_t run, const std::string &testcase) const;

        /**
         * Parses the test results and inserts them into the database.
         *
         * @param run the id of the run
         * @param results the json test results
         * @return amount of test cases inserted
         */
        [[nodiscard]] std::size_t
        parse_results(const runs::run &run, json results) const;
    };
}

#endif /* WEB_TESTS_MANAGER_H */
