/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */

#ifndef WEB_DATABASE_CONNECTION_H
#define WEB_DATABASE_CONNECTION_H

#include <memory>
#include <optional>
#include <pqxx/connection>
#include <string>

namespace database {
    /**
     * Connects to the database.
     *
     * @param str the connection string
     * @return the database connection
     */
    std::unique_ptr<pqxx::connection, void (*)(pqxx::connection *)>
    connect(const std::string &str);
}

#endif /* WEB_DATABASE_CONNECTION_H */