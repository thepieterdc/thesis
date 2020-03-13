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

std::uint_fast64_t
repositories::manager::create(const std::string &repository) const {
    // Create a new repository in the database.
    const std::string sql(
            "INSERT INTO repositories (url) VALUES(?)");
    const auto stmt = this->db.prepare(sql);
    stmt->bind_text(1, repository);

    // Return the id of the created repository.
    return this->db.insert(*stmt);
}

std::optional<std::uint_fast64_t>
repositories::manager::find(const std::string &url) const {
    // Get the id of the repository if it exists.
    const std::string sql(
            "SELECT id FROM repositories WHERE url=? LIMIT 1");
    const auto stmt = this->db.prepare(sql);
    stmt->bind_text(1, url);
    const auto found = database::connection::find(*stmt);

    // Validate the result of the query.
    if (found) {
        return std::make_optional(stmt->get_integer(0));
    }

    // Repository was not found.
    return std::nullopt;
}