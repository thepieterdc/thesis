/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */

#include <iostream>
#include <pqxx/pqxx>
#include "manager.h"

#define PREPARED_PREDICTION_FIND_ALL "prediction_find_all"
#define PREPARED_PREDICTION_FIND_SELECTED "prediction_find_selected"

predictions::manager::manager(pqxx::connection &db) : db(db) {
    this->db.prepare(PREPARED_PREDICTION_FIND_ALL,
                     "SELECT predictor_id, testorder FROM predictions WHERE run_id=$1");
    this->db.prepare(PREPARED_PREDICTION_FIND_SELECTED,
                     "SELECT predictor_id, testorder FROM predictions WHERE run_id=$1 AND selected=true LIMIT 1");
}

predictions::predictions_list
predictions::manager::find_all(const runs::run &run) const {
    // Start a transaction.
    pqxx::work tx(this->db);

    // Attempt to find the results.
    const auto result = tx.prepared(PREPARED_PREDICTION_FIND_ALL)
            (run.id).exec();

    // Commit the transaction.
    tx.commit();

    // Create the return list.
    predictions::predictions_list ret;

    // Iterate over the results.
    for (const auto &it : result) {
        const auto prediction = std::shared_ptr<predictions::prediction>(
                new predictions::prediction(
                        it["predictor_id"].as<std::uint_fast64_t>(),
                        it["testorder"].as<std::string>()
                )
        );
        ret.push_back(prediction);
    }

    return ret;
}

std::optional<predictions::prediction_ptr>
predictions::manager::find_selected(const runs::run &run) const {
    // Validate whether the run has already been predicted yet.
    if (run.predicted) {
        // Start a transaction.
        pqxx::work tx(this->db);

        // Find the selected prediction.
        const auto result = tx.prepared(PREPARED_PREDICTION_FIND_SELECTED)
                (run.id).exec();

        // Commit the transaction.
        tx.commit();

        // Validate the result of the query.
        if (!result.empty()) {
            const auto predictor_id =
                    result[0]["predictor_id"].as<std::uint_fast64_t>();
            const auto order_str = result[0]["testorder"].as<std::string>();
            return std::make_optional(predictions::prediction_ptr(
                    new predictions::prediction(predictor_id, order_str)
            ));
        }
    }

    return std::nullopt;
}