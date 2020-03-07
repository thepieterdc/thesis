/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */

#include "buffer.h"

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
        // Insert the coverage data into the database.
        const std::string sql(
                "INSERT INTO tests_coverage (test_id, sourcefile, from_line, to_line) VALUES(?, ?, ?, ?)"
        );
        const auto stmt = this->db.prepare(sql);
        stmt->bind_integer(1, this->test);
        stmt->bind_text(2, this->file);
        stmt->bind_integer(3, this->start_line);
        stmt->bind_integer(4, this->previous_line);
        this->db.insert(*stmt);
    }

    // Reset the data.
    this->previous_line = 0;
    this->start_line = 0;
}