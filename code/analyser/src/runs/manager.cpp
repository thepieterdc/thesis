/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */

#include <chrono>
#include <iostream>
#include <sstream>
#include "manager.h"

std::shared_ptr<runs::run>
runs::manager::create(const std::uint_fast64_t repository,
                      const std::string &commit_hash) const {
    // Get the current timestamp.
    const auto now = std::chrono::system_clock::now();
    const auto now_epoch = std::chrono::duration_cast<std::chrono::seconds>(
            now.time_since_epoch()
    ).count();

    // Create a new run in the database.
    const std::string sql(
            "INSERT INTO runs (repository_id, commit_hash, created_at) VALUES(?, ?, ?)");
    const auto stmt = this->db.prepare(sql);
    stmt->bind_integer(1, repository);
    stmt->bind_text(2, commit_hash);
    stmt->bind_integer(3, now_epoch);
    const auto id = this->db.insert(*stmt);

    // Return the created run.
    return std::shared_ptr<runs::run>(new runs::run(id, repository, now_epoch));
}

std::optional<std::shared_ptr<runs::run>>
runs::manager::find(std::uint_fast64_t id) const {
    // Get the run if it exists.
    const std::string sql(
            "SELECT id,repository,created_at FROM runs WHERE id=? LIMIT 1");
    const auto stmt = this->db.prepare(sql);
    stmt->bind_integer(1, id);
    const auto found = this->db.find(*stmt);

    // Validate the result of the query.
    if (found) {
        // Return the run.
        return std::make_optional(std::shared_ptr<runs::run>(new runs::run(
                stmt->get_integer(0),
                stmt->get_integer(1),
                stmt->get_integer(2)
        )));
    }

    // Run was not found.
    return std::nullopt;
}

std::optional<std::list<std::uint_fast64_t>>
runs::manager::find_order(const std::uint_fast64_t run) const {
    // Get the order if it exists.
    const std::string sql(
            "SELECT testorder FROM orders WHERE run_id=? LIMIT 1");
    const auto stmt = this->db.prepare(sql);
    stmt->bind_integer(1, run);
    const auto found = this->db.find(*stmt);

    // Validate the result of the query.
    if (found) {
        std::list<std::uint_fast64_t> order;

        // Parse the result.
        const auto order_str = stmt->get_text(0);
        std::istringstream iss(order_str);
        std::string test_id_str;
        // Iterate over the test ids.
        while (std::getline(iss, test_id_str, ',')) {
            // Parse the id to a number.
            order.push_back(std::stoi(test_id_str));
        }

        // Return the parsed order.
        return order;
    }

    // Order was not yet determined.
    return std::nullopt;
}