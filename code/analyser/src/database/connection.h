/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */

#ifndef ANALYSER_DATABASE_DATABASE_H
#define ANALYSER_DATABASE_DATABASE_H

#include <memory>
#include <optional>
#include <sqlite3.h>
#include <string>
#include "prepared_stmt.h"

namespace database {
    /**
     * Forward declare prepared statements.
     */
    class prepared_stmt;

    /**
     * Wrapper for the database connection.
     */
    class connection {
    private:
        sqlite3 *conn;

        /**
         * connection constructor.
         *
         * @param conn database connection
         */
        explicit connection(sqlite3 *conn) : conn(conn) {};

    public:
        /**
         * Creates a new database connection.
         *
         * @param file the sqlite database to open
         * @return the connection
         */
        static std::unique_ptr<connection> connect(const std::string &file);

        /**
         * connection destructor.
         */
        virtual ~connection();

        /**
         * Executes a statement.
         *
         * @param stmt the statement
         */
        static void exec(const database::prepared_stmt &stmt);

        /**
         * Executes a select statement for 1 value.
         *
         * @param stmt the statement
         * @return true if a match was found
         */
        static bool find(const database::prepared_stmt &stmt);

        /**
         * Executes an insert statement.
         *
         * @param stmt the statement
         * @return the insert id
         */
        std::uint_fast64_t insert(const database::prepared_stmt &stmt) const;

        /**
         * Creates a prepared statement.
         *
         * @param sql the query to prepare
         * @return the statement
         */
        std::unique_ptr<database::prepared_stmt>
        prepare(const std::string &sql) const;
    };
}

#endif /* ANALYSER_DATABASE_DATABASE_H */