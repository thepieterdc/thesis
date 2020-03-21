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
#include "predictions/manager.h"

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
    const auto predictions = predictions::manager(*db);
    const auto runs = runs::manager(*db);
    const auto tests = tests::manager(*db);

    // Find the run.
    const auto run_id = std::stoi(argv[2]);
    const auto run = runs.find(run_id);
    if (!run.has_value()) {
        // Run not found.
        util::logging::error("Run not found: %d", run_id);
        return EXIT_FAILURE;
    }

    // Find the order.
    const auto order_list = predictions.find_selected(**run);
    if (order_list.has_value()) {
        // Parse the order.
        std::list<std::string> order;
        for (const auto &it : (**order_list).get_order()) {
            // Get the test with the given id.
            const auto test = tests.find(it);

            // Validate the result.
            if (test.has_value()) {
                // Add the test case name to the list.
                order.push_back((*test)->testcase);
            } else {
                // Unknown test.
                util::logging::error(
                        "Test with the following id was not found: %d", it);
                return EXIT_FAILURE;
            }
        }

        // Print the list as json.
        json output;
        output["order"] = order;
        std::cout << output << std::endl;
    } else {
        // Order is not yet known.
        util::logging::error("Order not yet known for run #%d", (*run)->id);
        return EXIT_FAILURE;
    }

    return EXIT_SUCCESS;
}
