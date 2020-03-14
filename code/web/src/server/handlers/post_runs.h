/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */

#ifndef WEB_WEB_HANDLERS_POST_RUNS_H
#define WEB_WEB_HANDLERS_POST_RUNS_H

#include "../../runs/manager.h"
#include "../../coverage/manager.h"
#include "../../repositories/manager.h"

/**
 * Handles POST /runs.
 *
 * @param conn connection
 * @param repositories repositories manager
 * @param runs runs manager
 * @param body post body
 * @return true if handled
 */
bool handle_post_runs(struct mg_connection *conn,
                      const repositories::manager &repositories,
                      const runs::manager &runs,
                      json body);

#endif /* WEB_WEB_HANDLERS_POST_RUNS_H */
