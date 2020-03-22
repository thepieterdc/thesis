/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */

#ifndef WEB_PREDICTIONS_MANAGER_H
#define WEB_PREDICTIONS_MANAGER_H

#include "../database/connection.h"
#include "../runs/run.h"
#include "prediction.h"

namespace predictions {
    using predictions_list =
    std::vector<std::shared_ptr<predictions::prediction>>;

    /**
     * Manages predictions.
     */
    class manager {
    private:
        pqxx::connection &db;
    public:
        /**
         * manager constructor.
         *
         * @param db database connection
         */
        explicit manager(pqxx::connection &db);

        /**
         * manager destructor.
         */
        virtual ~manager() = default;

        /**
         * Finds all predictions of the given run.
         *
         * @param run the run
         * @return the predictions
         */
        [[nodiscard]] predictions_list find_all(const runs::run &run) const;

        /**
         * Finds the selected prediction of the given run.
         *
         * @param run the run
         * @return the prediction if found
         */
        [[nodiscard]] std::optional<predictions::prediction_ptr>
        find_selected(const runs::run &run) const;
    };
}

#endif /* WEB_REPOSITORIES_MANAGER_H */