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

// Lambda that closes pqxx connections.
const auto closer = [](pqxx::connection *conn) {
    conn->disconnect();
    delete conn;
};

std::unique_ptr<pqxx::connection, void (*)(pqxx::connection *)>
database::connect(const std::string &str) {
    // Create a connection.
    auto conn = std::unique_ptr<pqxx::connection, decltype(closer)>(
            new pqxx::connection(str), closer
    );

    // Ensure that the connection was successful.
    if (conn->is_open()) {
        return conn;
    }

    throw std::runtime_error("Failed connecting to the database.");
}