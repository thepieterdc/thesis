/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */

#ifndef WEB_WEB_RESPONSE_H
#define WEB_WEB_RESPONSE_H

#include <json.hpp>
#include <string>

using json = nlohmann::json;

namespace web {
    /**
     * Response of a http request.
     */
    class response {
    private:
        std::map<std::string, std::string> headers;
        std::string body = "";

        /**
         * Builds the header string.
         *
         * @return the header string
         */
        std::string build_header();

    public:
        uint_fast16_t code = 200;

        /**
         * Sets the json body.
         *
         * @param body body json
         */
        void body_json(const json &body);

        /**
         * Sends the response to the given connection.
         *
         * @param conn connection
         */
        void send(mg_connection *conn);
    };
}

#endif /* WEB_WEB_RESPONSE_H */
