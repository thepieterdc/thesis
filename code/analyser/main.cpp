/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */

#include <iostream>
#include "src/database/connection.h"
#include "src/runs/manager.h"
#include "src/tests/manager.h"
#include "src/coverage/manager.h"

/**
 * Main entrypoint.
 *
 * @param argc amount of arguments
 * @param argv arguments vector
 * @return successful
 */
int main(int argc, char **argv) {
    if (argc != 4) {
        throw std::runtime_error(
                "Syntax: ./analyser db.sqlite test_results.json /path/with/coverage/xmls"
        );
    }

    std::string test_results_file(argv[2]);
    std::string coverage_files(argv[3]);

    // Create a database connection.
    const auto db = database::connection::connect(argv[1]);

    // Start a new run.
    const auto runs_mgr = runs::manager(*db);
    const auto run = runs_mgr.create();

    // Parse the test results and save them to the database.
    const auto tests_mgr = tests::manager(*db);
    tests_mgr.parse(*run, test_results_file);

    // Parse the coverage logs and save them to the database.
    const auto coverage_mgr = coverage::manager(*db, tests_mgr);
    coverage_mgr.parse_all(*run, coverage_files);

    return EXIT_SUCCESS;
}
