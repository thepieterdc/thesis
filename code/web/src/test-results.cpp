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
#include "runs/manager.h"

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
        util::logging::error("Syntax: %s db_string run_id", argv[0]);
        return EXIT_FAILURE;
    }

    // Create a database connection.
    const auto db = database::connect(argv[1]);

    // Create managers.
    const auto runs = runs::manager(*db);

    // Find the run.
    const auto run_id = std::stoi(argv[2]);
    const auto run = runs.find(run_id);
    if (!run.has_value()) {
        // Run not found.
        util::logging::error("Run not found: %d", run_id);
        return EXIT_FAILURE;
    }

    // Parse the test results.
    json test_results;
    std::cin >> test_results;

    // Save the test results to the database.
    const auto results_parsed = tests::manager(*db)
            .parse_results(**run, test_results);

    // Print the parsed test results.
    util::logging::success("Parsed %d test results.", results_parsed);

    return EXIT_SUCCESS;
}
