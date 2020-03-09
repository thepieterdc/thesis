/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */

#ifndef ANALYSER_TESTS_MANAGER_H
#define ANALYSER_TESTS_MANAGER_H

#include <json.hpp>
#include "../database/connection.h"
#include "../runs/run.h"
#include "test.h"
#include "test_result.h"

using json = nlohmann::json;

namespace tests {
    /**
     * Manages tests.
     */
    class manager {
    private:
        const database::connection &db;

        /**
         * Creates a new test.
         *
         * @param testcase the name of the testcase
         * @return the created test
         */
        std::shared_ptr<tests::test> create(const std::string &testcase) const;

    public:
        /**
         * manager constructor.
         *
         * @param db database connection
         */
        explicit manager(database::connection &db) : db(db) {};

        /**
         * manager destructor.
         */
        virtual ~manager() = default;

        /**
         * Finds a test by the name of the testcase.
         *
         * @param testcase the name of the testcase
         * @return the test if found
         */
        std::optional<std::shared_ptr<tests::test>>
        find(const std::string &testcase) const;

        /**
         * Finds a test by its id.
         *
         * @param id the id of the testcase
         * @return the test if found
         */
        std::optional<std::shared_ptr<tests::test>>
        find(const std::uint_fast64_t id) const;

        /**
         * Finds a test result by the name of the testcase.
         *
         * @param run the id of the run
         * @param testcase the name of the testcase
         * @return the test result if found
         */
        std::optional<std::shared_ptr<tests::test_result>>
        find_result(std::uint_fast64_t run, const std::string &testcase) const;

        /**
         * Parses the test results and inserts them into the database.
         *
         * @param run the id of the run
         * @param results the json test results
         * @return amount of test cases inserted
         */
        std::size_t parse(std::uint_fast64_t run, json results) const;
    };
}

#endif /* ANALYSER_TESTS_MANAGER_H */
