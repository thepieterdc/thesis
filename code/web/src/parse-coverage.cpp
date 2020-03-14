/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */

#include <iostream>
#include "database/connection.h"
#include "util/logging.h"
#include "tests/manager.h"
#include "coverage/manager.h"

/**
 * Main entrypoint.
 *
 * @param argc amount of arguments
 * @param argv arguments vector
 * @return successful
 */
int main(int argc, char **argv) {
    if (argc != 4) {
        util::logging::error(
                "Syntax: %s database.db run_id folder_with_xmlfiles",
                argv[0]);
        return EXIT_FAILURE;
    }

    // Argument parsing.
    const auto run = std::stoi(argv[2]);
    const auto coverage_logs = std::string(argv[3]);

    // Create a database connection.
    const auto db = database::connection::connect(argv[1]);

    // Parse the coverage results and insert them into the database.
    const auto tests_mgr = tests::manager(*db);
    const auto coverage_parsed = coverage::manager(*db, tests_mgr)
            .parse_all(run, coverage_logs);

    // Print the parsed test results.
    util::logging::success("Parsed %d coverage reports.", coverage_parsed);

    return EXIT_SUCCESS;
}
