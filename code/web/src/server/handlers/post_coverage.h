/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */

#ifndef WEB_WEB_HANDLERS_POST_COVERAGE_H
#define WEB_WEB_HANDLERS_POST_COVERAGE_H

#include <string>
#include "../../coverage/manager.h"

struct coverage_upload_data {
    std::uint_fast64_t run;
    char *buf;
    std::FILE *fp;
    std::size_t size;
};

/**
 * Handles incoming multipart data chunks.
 *
 * @param conn the connection
 * @param data the data
 * @return true if handled
 */
bool handle_coverage_data(struct mg_connection *conn,
                          mg_http_multipart_part *multipart);

/**
 * Handles incoming multipart data.
 *
 * @param conn the connection
 * @param data the data
 * @return true if handled
 */
bool handle_coverage_finish(struct mg_connection *conn,
                            const coverage::manager &coverage);

/**
 * Handles the POST request that starts coverage uploading.
 *
 * @param conn connection
 * @param run id of the run
 * @return true if handled
 */
bool handle_post_coverage(struct mg_connection *conn, std::uint_fast64_t run);

#endif /* WEB_WEB_HANDLERS_POST_COVERAGE_H */
