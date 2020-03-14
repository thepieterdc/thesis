/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */

#include <sqlite3.h>
#include <iostream>
#include "connection.h"

std::unique_ptr<database::connection>
database::connection::connect(const std::string &file) {
    sqlite3 *db = nullptr;
    const int result = sqlite3_open(file.c_str(), &db);
    if (result > 0) {
        std::string error(sqlite3_errmsg(db));
        std::cerr << "Failed opening database: " << error << std::endl;
        exit(0);
    }

    return std::unique_ptr<connection>(new connection(db));
}

database::connection::~connection() {
    if (this->conn != nullptr) {
        sqlite3_close(this->conn);
        this->conn = nullptr;
    }
}

void database::connection::exec(const database::prepared_stmt &stmt) const {
    sqlite3_step(stmt.stmt);
}

bool database::connection::find(const database::prepared_stmt &stmt) const {
    const int result = sqlite3_step(stmt.stmt);
    if (result == SQLITE_ROW) {
        // Result found.
        return true;
    }

    if (result == SQLITE_DONE) {
        // No matches.
        return false;
    }

    // Query failed.
    throw std::runtime_error(sqlite3_errmsg(this->conn));
}

std::uint_fast64_t
database::connection::insert(const database::prepared_stmt &stmt) const {
    const int result = sqlite3_step(stmt.stmt);
    if (result != SQLITE_DONE) {
        throw std::runtime_error(sqlite3_errmsg(this->conn));
    }

    return sqlite3_last_insert_rowid(this->conn);
}

std::unique_ptr<database::prepared_stmt>
database::connection::prepare(const std::string &sql) const {
    sqlite3_stmt *stmt = nullptr;
    const int result = sqlite3_prepare_v3(this->conn, sql.c_str(), -1, 0,
                                          &stmt, nullptr);
    if (result != SQLITE_OK) {
        throw std::runtime_error(sqlite3_errmsg(this->conn));
    }

    return std::unique_ptr<database::prepared_stmt>(
            new database::prepared_stmt(stmt)
    );
}