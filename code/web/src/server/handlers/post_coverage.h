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
#include "../../predictions/meta_predictor.h"
#include "../../runs/manager.h"

/**
 * Handles the POST request that starts coverage uploading.
 *
 * @param conn connection
 * @param run id of the run
 * @param body the post body
 * @param coverage coverage manager
 * @param meta_predictor meta predictor
 * @param runs runs manager
 * @return true if handled
 */
bool handle_post_coverage(struct mg_connection *conn, std::uint_fast64_t run,
                          json body, const coverage::manager &coverage,
                          const predictions::meta_predictor &meta_predictor,
                          const runs::manager &runs);

#endif /* WEB_WEB_HANDLERS_POST_COVERAGE_H */
