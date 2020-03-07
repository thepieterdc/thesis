/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */

#ifndef ANALYSER_RUNS_MANAGER_H
#define ANALYSER_RUNS_MANAGER_H

#include "../database/connection.h"
#include "run.h"

namespace runs {
    /**
     * Manages runs.
     */
    class manager {
    private:
        const database::connection &db;
    public:
        /**
         * manager constructor.
         *
         * @param db database connection
         */
        explicit manager(database::connection &db) : db(db) {};

        /**
         * manager destructor.
         */
        virtual ~manager() = default;

        /**
         * Creates a new run.
         *
         * @return the created run
         */
        std::shared_ptr<runs::run> create() const;
    };
}

#endif /* ANALYSER_RUNS_MANAGER_H */
