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
         * Finds the id of the repository with the given url.
         *
         * @param url the url of the repository to find
         * @return the id if it exists
         */
        [[nodiscard]] std::optional<std::shared_ptr<predictions::prediction>>
        find_selected(const runs::run &run) const;
    };
}

#endif /* WEB_REPOSITORIES_MANAGER_H */