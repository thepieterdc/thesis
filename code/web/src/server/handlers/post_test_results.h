/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */

#ifndef WEB_WEB_HANDLERS_POST_TEST_RESULTS_H
#define WEB_WEB_HANDLERS_POST_TEST_RESULTS_H

#include "../../runs/manager.h"
#include "../../coverage/manager.h"
#include "../../predictions/meta_predictor.h"

/**
 * Handles POST /runs/{run}/test-results.
 *
 * @param conn connection
 * @param run id of the run
 * @param body the post body
 * @param runs runs manager
 * @param tests tests manager
 * @return true if handled
 */
bool handle_post_test_results(struct mg_connection *conn,
                              std::uint_fast64_t run,
                              json body,
                              const runs::manager &runs,
                              const tests::manager &tests);

#endif /* WEB_WEB_HANDLERS_POST_TEST_RESULTS_H */
