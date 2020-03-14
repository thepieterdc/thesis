/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */

#ifndef WEB_COVERAGE_BUFFER_H
#define WEB_COVERAGE_BUFFER_H

#include <utility>

#include "../database/connection.h"

namespace coverage {
    /**
     * Calculates coverage data.
     */
    class buffer {
    private:
        pqxx::connection &db;
        const std::string file;
        const std::uint_fast64_t test;

        std::uint_fast32_t previous_line = 0;
        std::uint_fast32_t start_line = 0;
    public:
        /**
         * buffer constructor.
         *
         * @param db database connection
         * @param file source file name
         * @param test id of the test
         */
        buffer(pqxx::connection &db, std::string file,
               const std::uint_fast64_t test) :
                db(db),
                file(std::move(file)),
                test(test) {};

        /**
         * manager destructor.
         */
        virtual ~buffer() = default;

        /**
         * Marks the given line as covered by the current test.
         *
         * @param line the line no
         */
        void cover(const std::uint_fast32_t line);

        /**
         * Flushes the buffer to the database if applicable.
         */
        void flush();
    };
}

#endif /* WEB_COVERAGE_BUFFER_H */