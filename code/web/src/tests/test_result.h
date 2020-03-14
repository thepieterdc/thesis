/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */

#ifndef WEB_TESTS_TEST_RESULT_H
#define WEB_TESTS_TEST_RESULT_H

#include <string>
#include <utility>

namespace tests {
    /**
     * A test.
     */
    class test_result {
    private:
        friend class manager;

        /**
         * test_result constructor.
         *
         * @param id id of the test result
         * @param run_id id of the test run
         * @param test_id id of the test
         * @param failed outcome of the test
         */
        test_result(std::uint_fast64_t id, std::uint_fast64_t run_id,
                    std::uint_fast64_t test_id, bool failed) :
                failed(failed),
                id(id),
                run_id(run_id),
                test_id(test_id) {};

    public:
        const bool failed;
        const std::uint_fast64_t id;
        const std::uint_fast64_t run_id;
        const std::uint_fast64_t test_id;

        /**
         * test_result destructor.
         */
        virtual ~test_result() = default;
    };
}

#endif /* WEB_TESTS_TEST_RESULT_H */
