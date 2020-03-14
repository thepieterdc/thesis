/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */

#ifndef WEB_COVERAGE_MANAGER_H
#define WEB_COVERAGE_MANAGER_H

#include "../database/connection.h"
#include "../runs/run.h"
#include "../tests/manager.h"

namespace coverage {
    /**
     * Manages coverage data.
     */
    class manager {
    private:
        pqxx::connection &db;
        const tests::manager &tests;

        /**
         * Parses the coverage results of one file and inserts it into the
         * database. A coverage path is only updated if it does not yet exist,
         * or if the test was successful.
         *
         * @param run current test run
         * @param contents contents of the file to parse
         */
        void parse(std::uint_fast64_t run, const std::string &contents) const;

    public:
        /**
         * manager constructor.
         *
         * @param db database connection
         */
        manager(pqxx::connection &db, const tests::manager &tests) :
                db(db),
                tests(tests) {};

        /**
         * manager destructor.
         */
        virtual ~manager() = default;

        /**
         * Gets whether coverage is available for the given test id.
         *
         * @param test_id the test id to find
         * @return true if coverage is known
         */
        [[nodiscard]] bool available(std::uint_fast64_t test_id) const;

        /**
         * Removes the coverage information for the given test.
         *
         * @param test_id the test
         */
        void clear(std::uint_fast64_t test_id) const;

        /**
         * Parses the coverage results and inserts them into the database. A
         * coverage path is only updated if it does not yet exist, or if the
         * test was successful.
         *
         * @param run current test run
         * @param zip archive containing the coverage results
         * @return amount of files parsed
         */
        std::size_t parse_all(std::uint_fast64_t run, std::FILE *zip) const;

        /**
         * Parses the coverage results and inserts them into the database. A
         * coverage path is only updated if it does not yet exist, or if the
         * test was successful.
         *
         * @param run current test run
         * @param path folder containing the coverage results
         * @return amount of files parsed
         */
        [[nodiscard]] std::size_t
        parse_all(std::uint_fast64_t run, const std::string &path) const;
    };
}

#endif /* WEB_COVERAGE_MANAGER_H */
