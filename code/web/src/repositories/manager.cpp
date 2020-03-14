/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */

#include <chrono>
#include <pqxx/transaction>
#include <iostream>
#include <sstream>
#include "manager.h"

#define PREPARED_REPO_CREATE "repositories_create"
#define PREPARED_REPO_FIND "repositories_find"

repositories::manager::manager(pqxx::connection &db) : db(db) {
    this->db.prepare(PREPARED_REPO_CREATE,
                     "INSERT INTO repositories (url) VALUES ($1) RETURNING id");
    this->db.prepare(PREPARED_REPO_FIND,
                     "SELECT id FROM repositories WHERE url=$1 LIMIT 1");
}

std::uint_fast64_t
repositories::manager::create(const std::string &repository) const {
    // Start a transaction.
    pqxx::work tx(this->db);

    // Create a new repository in the database.
    const auto result = tx.prepared(PREPARED_REPO_CREATE)(repository).exec();

    // Commit the transaction.
    tx.commit();

    // Return the id of the created repository.
    return result[0][0].as<std::uint_fast64_t>();
}

std::optional<std::uint_fast64_t>
repositories::manager::find(const std::string &url) const {
    // Start a transaction.
    pqxx::work tx(this->db);

    // Get the id of the repository if it exists.
    const auto result = tx.prepared(PREPARED_REPO_FIND)(url).exec();

    // Commit the transaction.
    tx.commit();

    // Validate the result of the query.
    if (!result.empty()) {
        return std::make_optional(result[0]["id"].as<std::uint_fast64_t>());
    }

    // Repository was not found.
    return std::nullopt;
}