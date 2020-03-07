/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */

#ifndef ANALYSER_DATABASE_PREPARED_STMT_H
#define ANALYSER_DATABASE_PREPARED_STMT_H

#include <memory>
#include <sqlite3.h>
#include <string>
#include "connection.h"

namespace database {
    class prepared_stmt {
    private:
        sqlite3_stmt *stmt;

        friend class connection;

        /**
         * prepared_stmt constructor.
         *
         * @param stmt the statement
         */
        explicit prepared_stmt(sqlite3_stmt *stmt) : stmt(stmt) {};

    public:
        /**
         * prepared_stmt destructor.
         */
        virtual ~prepared_stmt();

        /**
         * Binds a boolean to the wildcard at the given index.
         *
         * @param idx the index to match
         * @param value the value to bind
         */
        void bind_boolean(int idx, bool value);

        /**
         * Binds an integer to the wildcard at the given index.
         *
         * @param idx the index to match
         * @param value the value to bind
         */
        void bind_integer(int idx, std::uint_fast64_t value);

        /**
         * Binds a textual value to the wildcard at the given index.
         *
         * @param idx the index to match
         * @param value the value to bind
         */
        void bind_text(int idx, const std::string &value);

        /**
         * Gets the boolean at the given index.
         *
         * @param idx the index
         * @return the boolean value
         */
        bool get_boolean(int idx);

        /**
         * Gets the integer at the given index.
         *
         * @param idx the index
         * @return the integer value
         */
        std::uint_fast64_t get_integer(int idx);
    };
}

#endif /* ANALYSER_DATABASE_PREPARED_STMT_H */
