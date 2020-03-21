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
#include "server/server.h"

/**
 * Main entrypoint.
 *
 * @param argc amount of arguments
 * @param argv arguments vector
 * @return successful
 */
int main(int argc, char **argv) {
    if (argc != 3) {
        util::logging::error("Syntax: %s db_string port", argv[0]);
        return EXIT_FAILURE;
    }

    // Argument parsing.
    const auto port = std::stoi(argv[2]);

    // Create a database connection.
    const auto db = database::connect(argv[1]);

    // Create managers.
    const auto predictions = predictions::manager(*db);
    const auto repositories = repositories::manager(*db);
    const auto runs = runs::manager(*db);
    const auto tests = tests::manager(*db);
    const auto coverage = coverage::manager(*db, tests);

    // Create the webserver.
    auto server = web::server(port, coverage, predictions, repositories, runs,
                              tests);

    // Start the webserver.
    server.start();

    return EXIT_SUCCESS;
}
