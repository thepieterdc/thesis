/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */

#include <pqxx/pqxx>
#include "meta_predictor.h"
#include "../util/logging.h"

#define PREPARED_META_PREDICTOR_CREATE "meta_predictor_create"
#define PREPARED_META_PREDICTOR_EXISTS "meta_predictor_exists"
#define PREPARED_META_PREDICTOR_STATUS_QUO "meta_predictor_status_quo"
#define PREPARED_META_PREDICTOR_UPDATE "meta_predictor_update"

using predictor_duration = std::pair<std::uint_fast64_t, std::uint_fast64_t>;

/**
 * Driver function that sorts predictors based on their duration.
 *
 * @param a the first predictor
 * @param b the second predictor
 * @return true if a should be ordered before b
 */
bool duration_sort(const predictor_duration &a, const predictor_duration &b) {
    return a.second < b.second;
}

/**
 * Calculates the time until the first failing test is encountered.
 *
 * @param predictions the order predictions
 * @param results the results to consider
 * @return for every prediction, the duration until the first failure
 */
std::map<std::uint_fast64_t, std::uint_fast64_t>
find_first_failures(const predictions::predictions_list &predictions,
                    const tests::test_results &results) {
    std::map<std::uint_fast64_t, std::uint_fast64_t> ret;

    // Iterate over the predictions.
    for (const auto &pred : predictions) {
        ret[pred->predictor] = pred->first_failure(results);
    }

    return ret;
}

/**
 * Finds out whether any test has failed.
 *
 * @param results the results to consider
 * @return true if at least one test has failed
 */
bool has_failed_tests(const tests::test_results &results) {
    for (const auto &it : results) {
        if (it.second->failed) {
            return true;
        }
    }
    return false;
}

predictions::meta_predictor::meta_predictor(pqxx::connection &db,
                                            const predictions::manager &predictions,
                                            const tests::manager &tests) :
        db(db), predictions(predictions), tests(tests) {
    this->db.prepare(PREPARED_META_PREDICTOR_CREATE,
                     "INSERT INTO predictors_scores (repository_id, predictor_id, run_id) VALUES ($1, $2, $3)");
    this->db.prepare(PREPARED_META_PREDICTOR_EXISTS,
                     "SELECT run_id FROM predictors_scores WHERE repository_id=$1 LIMIT 1");
    this->db.prepare(PREPARED_META_PREDICTOR_STATUS_QUO,
                     "INSERT INTO predictors_scores (repository_id, predictor_id, score, run_id) VALUES ($1, $2, 0, $3) ON CONFLICT ON CONSTRAINT predictors_scores_pkey DO UPDATE SET run_id=$3");
    this->db.prepare(PREPARED_META_PREDICTOR_UPDATE,
                     "UPDATE predictors_scores SET run_id=$1, score=score+($2) WHERE repository_id=$3 AND predictor_id=$4");
}

void predictions::meta_predictor::update(const runs::run &run) const {
    // Fetch the test results of this run.
    const auto test_results = this->tests.find_results(run.id);

    // Fetch the predictions of this run.
    const auto run_predictions = this->predictions.find_all(run);

    // Get the last prediction score for this repository to find out whether
    // it has already been evaluated before.
    {
        // Start a transaction.
        pqxx::work tx(this->db);

        const auto result = tx.prepared(PREPARED_META_PREDICTOR_EXISTS)
                (run.repository_id).exec();
        if (result.empty()) {
            // Repository was never predicted before.
            for (const auto &it : run_predictions) {
                tx.prepared(PREPARED_META_PREDICTOR_CREATE)
                        (run.repository_id)(it->predictor)(run.id).exec();
            }

            // Commit the transaction.
            tx.commit();

            return;
        }

        const auto scored_run = result[0]["run_id"].as<std::uint_fast64_t>();
        if (scored_run >= run.id) {
            // Run has already been scored.
            return;
        }
    }

    // No failing test was found, don't update the scores.
    if (!has_failed_tests(test_results)) {
        // Start a transaction.
        pqxx::work tx(this->db);

        // Update the run id.
        for (const auto &it : run_predictions) {
            tx.prepared(PREPARED_META_PREDICTOR_STATUS_QUO)
                    (run.repository_id)(it->predictor)(run.id).exec();
        }

        // Commit the transaction.
        tx.commit();

        return;
    }

    // Determine the time until the first failure.
    const auto first_failures = find_first_failures(run_predictions,
                                                    test_results);

    // Create a vector of pairs of the durations so they can be sorted.
    std::vector<predictor_duration> predictor_durations;

    // Find the average duration until the first failure.
    std::uint_fast64_t avg_duration = 0;
    for (const auto &it : first_failures) {
        avg_duration += it.second;
        predictor_durations.emplace_back(std::make_pair(it.first, it.second));
    }
    avg_duration /= first_failures.size();

    // Sort the durations.
    std::sort(predictor_durations.begin(),
              predictor_durations.end(),
              duration_sort);

    // Start a transaction.
    pqxx::work tx(this->db);

    // Increase the scores of predictions above or equal to the average,
    const auto amt_predictors = predictor_durations.size();
    const std::uint_fast64_t amt_higher = std::count_if(
            predictor_durations.begin(),
            predictor_durations.end(),
            [avg_duration](predictor_duration d) {
                return d.second <= avg_duration;
            }
    );
    for (std::uint_fast64_t i = 0; i < amt_higher; ++i) {
        const auto predictor_id = predictor_durations[i].first;
        const std::int_fast64_t score = amt_higher - i;
        tx.prepared(PREPARED_META_PREDICTOR_UPDATE)
                (run.id)(score)(run.repository_id)(predictor_id).exec();
    }

    // Decrease the score of predictions lower than the average.
    for (std::uint_fast64_t i = amt_higher; i < amt_predictors; ++i) {
        const auto predictor_id = predictor_durations[i].first;
        const std::int_fast64_t score = -(i - amt_higher + 1);
        tx.prepared(PREPARED_META_PREDICTOR_UPDATE)
                (run.id)(score)(run.repository_id)(predictor_id).exec();
    }

    // Commit the transaction.
    tx.commit();
}