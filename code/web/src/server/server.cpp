/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */

#include <regex>
#include <stdexcept>
#include <utility>
#include "server.h"
#include "../util/logging.h"
#include "../runs/run.h"
#include "response.h"
#include "handlers/get_run.h"
#include "handlers/post_runs.h"
#include "handlers/post_test_results.h"
#include "handlers/post_coverage.h"

static std::regex coverage_logs_regex("/runs/([0-9]+)/coverage");
static std::regex order_regex("/runs/([0-9]+)");
static std::regex test_results_regex("/runs/([0-9]+)/test-results");

void web::server::handle(struct mg_connection *conn, int ev, void *ev_data) {
    const auto *server = static_cast<web::server *>(conn->mgr->user_data);

    // Handle the event.
    if (ev == MG_EV_HTTP_REQUEST) {
        // Parse the request.
        auto *const msg = static_cast<http_message *>(ev_data);
        const auto method = std::string(msg->method.p, msg->method.len);
        const auto uri = std::string(msg->uri.p, msg->uri.len);

        util::logging::notice("%s %s", method.c_str(), uri.c_str());

        // Handle the request.
        if (method == "GET") {
            if (server->handle_get(conn, uri)) {
                return;
            }
        } else if (method == "POST") {
            // Parse the postbody.
            const auto body = json::parse(
                    std::string(msg->body.p, msg->body.len));

            if (server->handle_post(conn, uri, body)) {
                return;
            }
        }

        // Event was not handled -> Send 404.
        web::response resp;
        resp.code = 404;
        resp.send(conn);
    }
}

bool web::server::handle_get(struct mg_connection *conn,
                             const std::string &uri) const {

    // Regex matcher.
    std::smatch matches;

    if (std::regex_search(uri, matches, order_regex)) {
        try {
            // Find the run id.
            const auto run = std::stoi(matches[1].str());

            // Handle the request.
            return handle_get_run(conn, run, this->predictions, this->runs,
                                  this->tests);
        } catch (std::invalid_argument &e) {
            // Create the response.
            web::response resp;
            resp.code = 400;
            resp.send(conn);
        }

        return true;
    }

    // No route matched.
    return false;
}

bool
web::server::handle_post(struct mg_connection *conn, const std::string &uri,
                         json body) const {
    // Regex matcher.
    std::smatch matches;

    // Create a new run.
    if (uri == "/runs") {
        return handle_post_runs(conn, this->repositories, this->runs,
                                std::move(body));
    } else if (std::regex_search(uri, matches, coverage_logs_regex)) {
        // Get the run id.
        const auto run_id = std::stoi(matches[1].str());

        // Handle the request.
        return handle_post_coverage(conn, run_id, std::move(body),
                                    this->coverage, this->meta_predictor, this->runs);
    } else if (std::regex_search(uri, matches, test_results_regex)) {
        // Find the run id.
        const auto run_id = std::stoi(matches[1].str());

        // Handle the request.
        return handle_post_test_results(conn, run_id, std::move(body),
                                        this->runs,
                                        this->tests);
    }

    return false;
}

web::server::server(const std::uint_fast16_t port,
                    const coverage::manager &coverage,
                    const predictions::meta_predictor &meta_predictor,
                    const predictions::manager &predictions,
                    const repositories::manager &repositories,
                    const runs::manager &runs,
                    const tests::manager &tests) :
        port(port),
        running(true),
        coverage(coverage),
        meta_predictor(meta_predictor),
        predictions(predictions),
        repositories(repositories),
        runs(runs),
        tests(tests) {
    // Initialise the webserver.
    this->mgr = (mg_mgr *) malloc(sizeof(mg_mgr));
    mg_mgr_init(this->mgr, this);

    // Bind to the port.
    auto *const conn = mg_bind(this->mgr, std::to_string(port).c_str(), handle);
    if (conn == nullptr) {
        throw std::runtime_error("Could not bind server to port.");
    }

    // Set up server parameters.
    mg_set_protocol_http_websocket(conn);
}

web::server::~server() {
    this->running = false;
    if (this->mgr != nullptr) {
        mg_mgr_free(this->mgr);
        free(this->mgr);
        this->mgr = nullptr;
    }
}

void web::server::start() const {
    util::logging::notice("Listening on port %d.", this->port);
    while (this->running) {
        mg_mgr_poll(this->mgr, 100);
    }
}