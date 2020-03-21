/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */

#ifndef WEB_WEB_HANDLERS_GET_RUN_H
#define WEB_WEB_HANDLERS_GET_RUN_H

#include "../../runs/manager.h"
#include "../../coverage/manager.h"
#include "../../predictions/manager.h"

/**
 * Handles GET /runs/{run}.
 *
 * @param conn connection
 * @param run id of the run
 * @param predictions predictions manager
 * @param runs runs manager
 * @param tests test manager
 * @return true if handled
 */
bool handle_get_run(struct mg_connection *conn, std::uint_fast64_t run,
                    const predictions::manager &predictions,
                    const runs::manager &runs, const tests::manager &tests);

#endif /* WEB_WEB_HANDLERS_GET_RUN_H */
