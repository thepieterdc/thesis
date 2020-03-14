/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */

#include <mongoose.h>
#include <sstream>
#include "response.h"

void web::response::body_json(const json &json_body) {
    // Set the content header.
    this->headers["Content-Type"] = "application/json";

    // Set the body.
    this->body = json_body.dump();
}

std::string web::response::build_header() {
    std::ostringstream data;
    // Set the status code.
    data << "HTTP/1.1 " << this->code << "\r\n";

    // Set the headers.
    for (const auto &header : this->headers) {
        data << header.first << ": " << header.second << "\r\n";
    }

    // Finalize by adding a newline.
    data << "\r\n";

    return data.str();
}

void web::response::send(struct mg_connection *conn) {
    // Set the content length.
    this->headers["Content-Length"] = std::to_string(this->body.size());

    // Parse the map of headers to a string.
    std::string headerstr = this->build_header();

    // Send the header and body.
    mg_printf(conn, "%s", headerstr.c_str());
    mg_printf(conn, "%s", this->body.c_str());

    // Terminate the connection.
    conn->flags |= MG_F_SEND_AND_CLOSE;
}
