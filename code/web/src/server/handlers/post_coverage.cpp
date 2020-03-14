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

bool handle_coverage_data(struct mg_connection *conn,
                          mg_http_multipart_part *multipart) {
    // Get the upload metadata.
    auto *data = static_cast<coverage_upload_data *>(conn->user_data);

    // Write the part to the temporary file.
    if (fwrite(multipart->data.p, 1, multipart->data.len, data->fp) !=
        multipart->data.len) {
        // Write failed, send an error response.
        web::response resp;
        resp.code = 500;
        resp.send(conn);
        std::cout << "fail" << std::endl;
    }

    return true;
}

bool handle_coverage_finish(struct mg_connection *conn,
                            const coverage::manager &coverage) {
    // Create the response.
    web::response resp;

    // Get the upload metadata.
    auto *data = static_cast<coverage_upload_data *>(conn->user_data);

    // Parse the coverage logs.
    coverage.parse_all(data->run, data->fp);

    // Successful.
    resp.code = 204;
    resp.send(conn);

    // Memory cleanup.
    fclose(data->fp);
    free(data->buf);
    free(data);
    conn->user_data = nullptr;

    return true;
}

bool handle_post_coverage(struct mg_connection *conn, std::uint_fast64_t run) {
    // Get the upload metadata.
    auto *data = static_cast<coverage_upload_data *>(conn->user_data);
    if (data == nullptr) {
        data = static_cast<struct coverage_upload_data *>(
                calloc(1, sizeof(struct coverage_upload_data)));
        data->buf = nullptr;
        data->fp = open_memstream(&data->buf, &data->size);
        data->run = run;

        // Verify that the temporary file was created.
        if (data->fp == nullptr) {
            // Send an error response.
            web::response resp;
            resp.code = 500;
            resp.send(conn);
            free(data);
            return true;
        }

        // Store the data.
        conn->user_data = data;
    }

    return true;
}