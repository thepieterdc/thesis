/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */

#include <pqxx/transaction>
#include "buffer.h"

#define PREPARED_COVERAGE_CREATE "coverage_create"

coverage::buffer::buffer(pqxx::connection &db, std::string file,
                         const std::uint_fast64_t test) :
        db(db), file(std::move(file)), test(test) {
    this->db.prepare(PREPARED_COVERAGE_CREATE,
                     "INSERT INTO tests_coverage (test_id, sourcefile, from_line, to_line) VALUES($1, $2, $3, $4)"
    );
}

void coverage::buffer::cover(const std::uint_fast32_t line) {
    if (this->start_line == 0) {
        // New cover block.
        this->start_line = line;
        this->previous_line = line;
        return;
    }

    if (this->previous_line + 1 == line) {
        // Ongoing cover block.
        this->previous_line = line;
        return;
    }

    // New cover block.
    this->flush();
    this->cover(line);
}

void coverage::buffer::flush() {
    if (this->previous_line != 0) {
        // Start a transaction.
        pqxx::work tx(this->db);

        // Insert the coverage data into the database.

        // Create a new repository in the database.
        const auto result = tx.prepared(PREPARED_COVERAGE_CREATE)(this->test)
                (this->file)(this->start_line)(this->previous_line).exec();

        // Commit the transaction.
        tx.commit();
    }

    // Reset the data.
    this->previous_line = 0;
    this->start_line = 0;
}