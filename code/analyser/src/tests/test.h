/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */

#ifndef ANALYSER_TESTS_TEST_H
#define ANALYSER_TESTS_TEST_H

#include <string>
#include <utility>

namespace tests {
    /**
     * A test.
     */
    class test {
    private:
        friend class manager;

        /**
         * test constructor.
         *
         * @param id id of the test
         * @param testcase the name of the test
         */
        test(std::uint_fast64_t id, std::string testcase) :
                id(id),
                testcase(std::move(testcase)) {};

    public:
        const std::uint_fast64_t id;
        const std::string testcase;

        /**
         * test destructor.
         */
        virtual ~test() = default;
    };
}

#endif /* ANALYSER_TESTS_TEST_H */
