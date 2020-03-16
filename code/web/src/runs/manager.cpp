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
#define PREPARED_RUN_FIND_ORDER "run_find_order"

runs::manager::manager(pqxx::connection &db) : db(db) {
    this->db.prepare(PREPARED_RUN_CREATE,
                     "INSERT INTO runs (repository_id, base_path, commit_hash) VALUES($1, $2, $3) RETURNING id");
    this->db.prepare(PREPARED_RUN_FIND,
                     "SELECT id,repository_id,created_at FROM runs WHERE id=$1 LIMIT 1");
    this->db.prepare(PREPARED_RUN_FIND_ORDER,
                     "SELECT testorder FROM runs WHERE id=$1 LIMIT 1");
}

std::shared_ptr<runs::run>
runs::manager::create(const std::uint_fast64_t repository,
                      const std::string &base_path,
                      const std::string &commit_hash) const {
    // Start a transaction.
    pqxx::work tx(this->db);

    // Create a new run in the database.
    const auto result = tx.prepared(PREPARED_RUN_CREATE)(repository)
            (base_path)(commit_hash).exec();

    // Commit the transaction.
    tx.commit();

    const auto id = result[0][0].as<std::uint_fast64_t>();

    // Return the created run.
    return std::shared_ptr<runs::run>(new runs::run(id, repository));
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
                result[0]["repository_id"].as<std::uint_fast64_t>()
        )));
    }

    // Run was not found.
    return std::nullopt;
}

std::optional<std::list<std::uint_fast64_t>>
runs::manager::find_order(const std::uint_fast64_t run) const {
    // Start a transaction.
    pqxx::work tx(this->db);

    // Get the order if it exists.
    const auto result = tx.prepared(PREPARED_RUN_FIND_ORDER)(run).exec();

    // Commit the transaction.
    tx.commit();

    // Validate the result of the query.
    if (!result.empty() && !result[0]["testorder"].is_null()) {
        std::list<std::uint_fast64_t> order;

        // Parse the result.
        const auto order_str = result[0]["testorder"].as<std::string>();
        std::istringstream iss(order_str);
        std::string test_id_str;
        // Iterate over the test ids.
        while (std::getline(iss, test_id_str, ',')) {
            // Parse the id to a number.
            order.push_back(std::stoi(test_id_str));
        }

        // Return the parsed order.
        return std::make_optional(order);
    }

    // Order was not yet determined.
    return std::nullopt;
}