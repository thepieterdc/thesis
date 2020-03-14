/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */

#ifndef WEB_RUNS_RUN_H
#define WEB_RUNS_RUN_H

namespace runs {
    /**
     * A test run.
     */
    class run {
    private:
        friend class manager;

        /**
         * run constructor.
         *
         * @param id id of the run
         * @param repository_id if of the repository
         */
        run(std::uint_fast64_t id, std::uint_fast64_t repository_id) :
                id(id),
                repository_id(repository_id) {};

    public:
        const std::uint_fast64_t id;
        const std::uint_fast64_t repository_id;

        /**
         * run destructor.
         */
        virtual ~run() = default;
    };
}

#endif /* WEB_RUNS_RUN_H */
