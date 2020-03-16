/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */

#ifndef WEB_RUNS_MANAGER_H
#define WEB_RUNS_MANAGER_H

#include <list>
#include "../database/connection.h"
#include "run.h"

namespace runs {
    /**
     * Manages runs.
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
         * Creates a new run.
         *
         * @param repository id of the repository
         * @param base_path base path of the sources
         * @param commit_hash hash of the commit that triggered this run
         * @return the created run
         */
        [[nodiscard]] std::shared_ptr<runs::run> create(
                std::uint_fast64_t repository,
                const std::string &base_path,
                const std::string &commit_hash) const;

        /**
         * Gets the order that with the given id.
         *
         * @param id the id of the run
         * @return the run if it exists
         */
        [[nodiscard]] std::optional<std::shared_ptr<runs::run>>
        find(std::uint_fast64_t id) const;

        /**
         * Gets the order that was calculated for the given run.
         *
         * @param run the id of the run
         * @return the order if it exists
         */
        [[nodiscard]] std::optional<std::list<std::uint_fast64_t>>
        find_order(std::uint_fast64_t run) const;
    };
}

#endif /* WEB_RUNS_MANAGER_H */