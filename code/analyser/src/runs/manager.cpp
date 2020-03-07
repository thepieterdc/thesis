/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */

#include <chrono>
#include <iostream>
#include "manager.h"

std::shared_ptr<runs::run> runs::manager::create() const {
    // Get the current timestamp.
    const auto now = std::chrono::system_clock::now();
    const auto now_epoch = std::chrono::duration_cast<std::chrono::seconds>(
            now.time_since_epoch()
    ).count();

    // Create a new run in the database.
    const std::string sql("INSERT INTO runs (created_at) VALUES(?)");
    const auto stmt = this->db.prepare(sql);
    stmt->bind_integer(1, now_epoch);
    const auto id = this->db.insert(*stmt);

    // Return the created run.
    return std::shared_ptr<runs::run>(new runs::run(id, now_epoch));
}