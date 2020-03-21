/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */

#include <iostream>
#include <pqxx/transaction>
#include "manager.h"

#define PREPARED_PREDICTION_FIND_SELECTED "prediction_find_selected"

predictions::manager::manager(pqxx::connection &db) : db(db) {
    this->db.prepare(PREPARED_PREDICTION_FIND_SELECTED,
                     "SELECT testorder FROM predictions WHERE run_id=$1 AND selected=true LIMIT 1");
}

std::optional<std::shared_ptr<predictions::prediction> >
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
            const auto order_str = result[0]["testorder"].as<std::string>();
            return std::make_optional(std::shared_ptr<predictions::prediction>(
                    new predictions::prediction(order_str)
            ));
        }
    }

    return std::nullopt;
}