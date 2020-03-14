/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */

#include <json.hpp>
#include <iostream>
#include "database/connection.h"
#include "util/logging.h"
#include "tests/manager.h"

using json = nlohmann::json;

/**
 * Main entrypoint.
 *
 * @param argc amount of arguments
 * @param argv arguments vector
 * @return successful
 */
int main(int argc, char **argv) {
    if (argc != 3) {
        util::logging::error("Syntax: %s database.db run_id", argv[0]);
        return EXIT_FAILURE;
    }

    // Argument parsing.
    const auto run = std::stoi(argv[2]);

    // Create a database connection.
    const auto db = database::connection::connect(argv[1]);

    // Parse the test results.
    json test_results;
    std::cin >> test_results;

    // Save the test results to the database.
    const auto results_parsed = tests::manager(*db).parse(run, test_results);

    // Print the parsed test results.
    util::logging::success("Parsed %d test results.", results_parsed);

    return EXIT_SUCCESS;
}
