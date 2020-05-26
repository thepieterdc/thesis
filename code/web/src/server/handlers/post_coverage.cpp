/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */

#include <mongoose.h>
#include <iostream>
#include <thread>
#include "post_coverage.h"
#include "../response.h"

/**
 * Updates the prediction scores for the given run.
 *
 * @param mp the meta predictor instance
 * @param run the run
 */
void update_mp(const predictions::meta_predictor &mp, const runs::run &run) {
    mp.update(run);
}

bool handle_post_coverage(struct mg_connection *conn, std::uint_fast64_t run_id,
                          json body, const coverage::manager &coverage,
                          const predictions::meta_predictor &meta_predictor,
                          const runs::manager &runs) {
    // Create the response.
    web::response resp;

    // Get the run.
    const auto run = runs.find(run_id);
    if (!run.has_value()) {
        resp.code = 404;
        resp.send(conn);
        return true;
    }

    // Save the coverage data.
    const auto parsed = coverage.parse(run_id, std::move(body));

    // Run the meta predictor.
    std::thread mp_thread(update_mp, meta_predictor, **run);
    mp_thread.detach();

    // Finish the response.
    resp.code = 200;
    resp.body_json({{"parsed", parsed}});
    resp.send(conn);

    return true;
}