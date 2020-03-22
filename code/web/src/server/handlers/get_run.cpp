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
#include "../../predictions/manager.h"

bool handle_get_run(struct mg_connection *conn, const std::uint_fast64_t run_id,
                    const predictions::manager &predictions,
                    const runs::manager &runs, const tests::manager &tests) {
    // Create the response.
    web::response resp;

    // Find the run.
    const auto run = runs.find(run_id);
    if (!run.has_value()) {
        // Run not found.
        resp.code = 404;
        resp.send(conn);
        return true;
    }

    // Get the order if it exists.
    const auto prediction = predictions.find_selected(**run);
    if (prediction.has_value()) {
        // Parse the order.
        std::list<std::string> order;
        bool valid = true;
        for (const auto &it : (*prediction)->testorder) {
            // Get the test with the given id.
            const auto test = tests.find(it);

            // Validate the result.
            if (test.has_value()) {
                // Add the test case name to the list.
                order.push_back((*test)->testcase);
            } else {
                // Unknown test.
                util::logging::error(
                        "Test with the following id was not found: %d",
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
