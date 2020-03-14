/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */

#ifndef ANALYSER_WEB_HANDLERS_POST_TEST_RESULTS_H
#define ANALYSER_WEB_HANDLERS_POST_TEST_RESULTS_H

#include "../../runs/manager.h"
#include "../../coverage/manager.h"

/**
 * Handles POST /runs/{run}/test-results.
 *
 * @param conn connection
 * @param run id of the run
 * @param tests tests manager
 * @return true if handled
 */
bool handle_post_test_results(struct mg_connection *conn,
                              std::uint_fast64_t run,
                              json body,
                              const tests::manager &tests);

#endif /* ANALYSER_WEB_HANDLERS_POST_TEST_RESULTS_H */
