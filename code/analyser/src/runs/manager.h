/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */

#ifndef ANALYSER_RUNS_MANAGER_H
#define ANALYSER_RUNS_MANAGER_H

#include <list>
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
         * @param commit_hash hash of the commit that triggered this run
         * @return the created run
         */
        std::shared_ptr<runs::run> create(const std::string &commit_hash) const;

        /**
         * Gets the order that was calculated for the given run.
         *
         * @param run the id of the run
         * @return the order if it exists
         */
        std::optional<std::list<std::uint_fast64_t>>
        find_order(std::uint_fast64_t run) const;
    };
}

#endif /* ANALYSER_RUNS_MANAGER_H */