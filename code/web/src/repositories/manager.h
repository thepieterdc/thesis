/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */

#ifndef WEB_REPOSITORIES_MANAGER_H
#define WEB_REPOSITORIES_MANAGER_H

#include "../database/connection.h"

namespace repositories {
    /**
     * Manages repositories.
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
        explicit manager(pqxx::connection &db) : db(db) {};

        /**
         * manager destructor.
         */
        virtual ~manager() = default;

        /**
         * Creates a new repository.
         *
         * @param url url to the repository
         * @return the id of the created repository
         */
        [[nodiscard]] std::uint_fast64_t create(const std::string &url) const;

        /**
         * Finds the id of the repository with the given url.
         *
         * @param url the url of the repository to find
         * @return the id if it exists
         */
        [[nodiscard]] std::optional<std::uint_fast64_t>
        find(const std::string &url) const;
    };
}

#endif /* WEB_REPOSITORIES_MANAGER_H */