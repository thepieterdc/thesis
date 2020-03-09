/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */

#include <iostream>
#include "web/server.h"
#include "util/logging.h"
#include "database/connection.h"

/**
 * Main entrypoint.
 *
 * @param argc amount of arguments
 * @param argv arguments vector
 * @return successful
 */
int main(int argc, char **argv) {
    if (argc != 3) {
        util::logging::error("Syntax: %s database.db port", argv[0]);
        return EXIT_FAILURE;
    }

    // Argument parsing.
    const auto port = std::stoi(argv[2]);

    // Create a database connection.
    const auto db = database::connection::connect(argv[1]);

    // Create managers.
    const auto runs = runs::manager(*db);
    const auto tests = tests::manager(*db);
    const auto coverage = coverage::manager(*db, tests);

    // Create the webserver.
    auto server = web::server(port, runs, tests, coverage);

    // Start the webserver.
    server.start();

    return EXIT_SUCCESS;
}
