/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */

#include "post_test_results.h"
#include "../response.h"

bool handle_post_test_results(struct mg_connection *conn,
                              const std::uint_fast64_t run,
                              json body,
                              const tests::manager &tests) {
    // Create the response.
    web::response resp;

    // Save the test results.
    const auto parsed = tests.parse(run, std::move(body));

    // Finish the response.
    resp.code = 204;
    resp.body_json({{"parsed", parsed}});
    resp.send(conn);

    return true;
}
