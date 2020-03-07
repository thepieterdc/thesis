/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */

#include "prepared_stmt.h"

database::prepared_stmt::~prepared_stmt() {
    if (this->stmt != nullptr) {
        sqlite3_finalize(this->stmt);
        this->stmt = nullptr;
    }
}

void database::prepared_stmt::bind_boolean(int idx, bool value) {
    const int result = sqlite3_bind_int64(this->stmt, idx, value ? 1 : 0);
    if (result != SQLITE_OK) {
        throw std::runtime_error(
                "Failed binding wildcard at index: " + std::to_string(idx));
    }
}

void database::prepared_stmt::bind_integer(int idx, std::uint_fast64_t value) {
    const int result = sqlite3_bind_int64(this->stmt, idx, value);
    if (result != SQLITE_OK) {
        throw std::runtime_error(
                "Failed binding wildcard at index: " + std::to_string(idx));
    }
}

void database::prepared_stmt::bind_text(int idx, const std::string &value) {
    const int result = sqlite3_bind_text(this->stmt, idx, value.c_str(),
                                         value.length(), SQLITE_STATIC);
    if (result != SQLITE_OK) {
        throw std::runtime_error(
                "Failed binding wildcard at index: " + std::to_string(idx));
    }
}

bool database::prepared_stmt::get_boolean(int idx) {
    return sqlite3_column_int64(this->stmt, idx) == 1;
}

std::uint_fast64_t database::prepared_stmt::get_integer(int idx) {
    return sqlite3_column_int64(this->stmt, idx);
}