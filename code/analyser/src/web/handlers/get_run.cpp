/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */

#include "get_run.h"
#include "../response.h"
#include "../../util/logging.h"

bool handle_get_run(struct mg_connection *conn, const std::uint_fast64_t run,
                    const runs::manager &runs, const tests::manager &tests) {
    // Create the response.
    web::response resp;

    // Get the order if it exists.
    const auto opt_order = runs.find_order(run);
    if (opt_order.has_value()) {
        // Order is known.
        const auto &order_list = opt_order.value();

        // Parse the order.
        std::list<std::string> order;
        bool valid = true;
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
                        "Test with the following id was not found: ",
                        it);
                resp.code = 500;
                valid = false;
                break;
            }
        }

        if (valid) {
            // Return the list as json.
            resp.body_json({{"order", order}});
        }
    } else {
        // Order is not yet known.
        resp.code = 206;
    }

    resp.send(conn);
    return true;
}
