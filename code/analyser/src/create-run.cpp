/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */

#include "database/connection.h"
#include "runs/manager.h"
#include "util/logging.h"
#include "repositories/manager.h"

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
                "Syntax: %s database.db repository_url commit_hash", argv[0]);
        return EXIT_FAILURE;
    }

    // Create a database connection.
    const auto db = database::connection::connect(argv[1]);

    // Find the repository.
    const auto repositories = repositories::manager(*db);
    const auto opt_repository = repositories.find(argv[2]);
    const auto repository = opt_repository.has_value()
                            ? opt_repository.value()
                            : repositories.create(argv[2]);

    // Create the run.
    const auto run = runs::manager(*db).create(repository, argv[3]);

    // Print the created job.
    util::logging::success("Run #%d created.", run->id);

    return EXIT_SUCCESS;
}
