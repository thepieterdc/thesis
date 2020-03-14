/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */

#include "post_runs.h"
#include "../response.h"

bool handle_post_runs(struct mg_connection *conn,
                      const repositories::manager &repositories,
                      const runs::manager &runs,
                      json body) {
    // Create the response.
    web::response resp;

    // Find the repository.
    if (body["commit_hash"].is_null() || body["repository"].is_null()) {
        resp.code = 400;
        resp.send(conn);
        return true;
    }

    // Find the repository.
    const auto repository_url = body["repository"].get<std::string>();
    const auto opt_repository = repositories.find(repository_url);
    const auto repository = opt_repository.has_value()
                            ? opt_repository.value()
                            : repositories.create(repository_url);

    // Create the run.
    const auto commit_hash = body["commit_hash"].get<std::string>();
    const auto run = runs.create(repository, commit_hash);

    // Build the response body.
    json respbody = {{"id", run->id}};

    // Finish the response.
    resp.code = 201;
    resp.body_json(respbody);
    resp.send(conn);

    return true;
}
