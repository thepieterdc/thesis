/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */

#include <iostream>
#include <pqxx/transaction>
#include "manager.h"

#define PREPARED_RUN_CREATE "run_create"
#define PREPARED_RUN_FIND "run_find"

runs::manager::manager(pqxx::connection &db) : db(db) {
    this->db.prepare(PREPARED_RUN_CREATE,
                     "INSERT INTO runs (repository_id, commit_hash) VALUES($1, $2) RETURNING id");
    this->db.prepare(PREPARED_RUN_FIND,
                     "SELECT id,predicted,repository_id,created_at FROM runs WHERE id=$1 LIMIT 1");
}

std::shared_ptr<runs::run>
runs::manager::create(const std::uint_fast64_t repository,
                      const std::string &commit_hash) const {
    // Start a transaction.
    pqxx::work tx(this->db);

    // Create a new run in the database.
    const auto result = tx.prepared(PREPARED_RUN_CREATE)(repository)
            (commit_hash).exec();

    // Commit the transaction.
    tx.commit();

    // Return the created run.
    return std::shared_ptr<runs::run>(new runs::run(
            result[0]["id"].as<std::uint_fast64_t>(),
            false,
            repository
    ));
}

std::optional<std::shared_ptr<runs::run>>
runs::manager::find(std::uint_fast64_t id) const {
    // Start a transaction.
    pqxx::work tx(this->db);

    // Get the run if it exists.
    const auto result = tx.prepared(PREPARED_RUN_FIND)(id).exec();

    // Commit the transaction.
    tx.commit();

    // Validate the result of the query.
    if (!result.empty()) {
        // Return the run.
        return std::make_optional(std::shared_ptr<runs::run>(new runs::run(
                result[0]["id"].as<std::uint_fast64_t>(),
                result[0]["predicted"].as<bool>(),
                result[0]["repository_id"].as<std::uint_fast64_t>()
        )));
    }

    // Run was not found.
    return std::nullopt;
}