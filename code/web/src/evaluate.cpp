/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */

#include "database/connection.h"
#include "predictions/meta_predictor.h"
#include "predictions/manager.h"
#include "runs/manager.h"
#include "tests/manager.h"
#include "util/logging.h"

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
    const auto predictions = predictions::manager(*db);
    const auto runs = runs::manager(*db);
    const auto tests = tests::manager(*db);
    const auto meta_predictor = predictions::meta_predictor(
            *db, predictions, tests);

    // Find the run.
    const auto run_id = std::stoi(argv[2]);
    const auto run = runs.find(run_id);
    if (!run.has_value()) {
        // Run not found.
        util::logging::error("Run not found: %d", run_id);
        return EXIT_FAILURE;
    }

    meta_predictor.update(**run);

    return EXIT_SUCCESS;
}
