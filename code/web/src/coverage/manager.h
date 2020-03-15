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

    public:
        /**
         * manager constructor.
         *
         * @param db database connection
         */
        manager(pqxx::connection &db, const tests::manager &tests);

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
         * @param data coverage data
         * @return amount of files parsed
         */
        [[nodiscard]] std::size_t
        parse(std::uint_fast64_t run, json data) const;
    };
}

#endif /* WEB_COVERAGE_MANAGER_H */
