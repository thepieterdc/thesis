/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */

#ifndef ANALYSER_RUNS_RUN_H
#define ANALYSER_RUNS_RUN_H

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
         * @param created_at creation timestamp
         */
        run(std::uint_fast64_t id, std::uint_fast64_t created_at) :
                created_at(created_at),
                id(id) {};

    public:
        const std::uint_fast64_t created_at;
        const std::uint_fast64_t id;

        /**
         * run destructor.
         */
        virtual ~run() = default;
    };
}

#endif /* ANALYSER_RUNS_RUN_H */
