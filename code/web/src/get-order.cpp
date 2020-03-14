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
        util::logging::error("Syntax: %s database.db run_id", argv[0]);
        return EXIT_FAILURE;
    }

    // Argument parsing.
    const auto run = std::stoi(argv[2]);

    // Create a database connection.
    const auto db = database::connection::connect(argv[1]);

    // Create managers.
    const auto runs = runs::manager(*db);
    const auto tests = tests::manager(*db);

    // Get the order.
    const auto opt_order = runs.find_order(run);
    if (opt_order.has_value()) {
        // Order is known.
        const auto &order_list = opt_order.value();

        // Parse the order.
        std::list<std::string> order;
        for (const auto &it : order_list) {
            // Get the test with the given id.
            const auto opt_test = tests.find(it);

            // Validate the result.
            if (opt_test.has_value()) {
                // Add the test case name to the list.
                order.push_back(opt_test.value()->testcase);
            } else {
                // Unknown test.
                util::logging::error(
                        "Test with the following id was not found: ", it);
                return EXIT_FAILURE;
            }
        }

        // Print the list as json.
        json output;
        output["order"] = order;
        std::cout << output << std::endl;
    } else {
        // Order is not yet known.
        util::logging::error("Order not yet known for run #", run);
        return EXIT_FAILURE;
    }

    return EXIT_SUCCESS;
}
