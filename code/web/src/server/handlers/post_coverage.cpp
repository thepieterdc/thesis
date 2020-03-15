/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */

#include <mongoose.h>
#include <iostream>
#include "post_coverage.h"
#include "../response.h"

bool handle_post_coverage(struct mg_connection *conn, std::uint_fast64_t run,
                          json body, const coverage::manager &coverage) {
    // Create the response.
    web::response resp;

    // Save the coverage data.
    const auto parsed = coverage.parse(run, std::move(body));

    // Finish the response.
    resp.code = 200;
    resp.body_json({{"parsed", parsed}});
    resp.send(conn);

    return true;
}