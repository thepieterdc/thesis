/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */

#ifndef WEB_WEB_SERVER_H
#define WEB_WEB_SERVER_H

#include <cstdint>
#include <json.hpp>
#include <mongoose.h>
#include "../runs/manager.h"
#include "../coverage/manager.h"
#include "../repositories/manager.h"
#include "../predictions/manager.h"
#include "../predictions/meta_predictor.h"

using json = nlohmann::json;

namespace web {
    /**
     * Wrapper for the database connection.
     */
    class server {
    private:
        const std::uint_fast16_t port;
        bool running;

        const coverage::manager &coverage;
        const predictions::meta_predictor &meta_predictor;
        const predictions::manager &predictions;
        const repositories::manager &repositories;
        const runs::manager &runs;
        const tests::manager &tests;

        struct mg_mgr *mgr;

        /**
         * Handles the given request.
         *
         * @param conn connection
         * @param ev event
         * @param ev_data event data
         */
        static void handle(struct mg_connection *conn, int ev, void *ev_data);

        /**
         * Handles HTTP/GET methods.
         *
         * @param conn connection
         * @param uri the uri path
         * @return true if response was sent to client
         */
        bool
        handle_get(struct mg_connection *conn, const std::string &uri) const;

        /**
         * Handles HTTP/POST methods.
         *
         * @param conn connection
         * @param uri the uri path
         * @param body the request body
         * @return true if response was sent to client
         */
        bool handle_post(struct mg_connection *conn, const std::string &uri,
                         json body) const;

    public:
        /**
         * server constructor.
         *
         * @param port web server port
         * @param meta_predictor meta predictor
         * @param repositories repositories manager
         * @param runs runs manager
         * @param tests tests manager
         * @param coverage coverage manager
         */
        explicit server(std::uint_fast16_t port,
                        const coverage::manager &coverage,
                        const predictions::meta_predictor &meta_predictor,
                        const predictions::manager &predictions,
                        const repositories::manager &repositories,
                        const runs::manager &runs,
                        const tests::manager &tests);

        /**
         * server destructor.
         */
        virtual ~server();

        /**
         * Starts the server.
         */
        void start() const;
    };
}

#endif /* WEB_WEB_SERVER_H */