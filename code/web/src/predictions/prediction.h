/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */

#ifndef WEB_PREDICTIONS_PREDICTION_H
#define WEB_PREDICTIONS_PREDICTION_H

#include <list>
#include <string>
#include <utility>
#include "../tests/manager.h"

namespace predictions {
    // Forward declaration.
    class prediction;

    using prediction_ptr = std::shared_ptr<predictions::prediction>;

    /**
     * A prediction.
     */
    class prediction {
    private:
        friend class manager;

        /**
         * prediction constructor.
         *
         * @param predictor the id of the predictor
         * @param testorder the predicted order
         */
        explicit prediction(std::uint_fast64_t predictor,
                            const std::string &testorder);

    public:
        const std::uint_fast64_t predictor;
        std::vector<std::uint_fast64_t> testorder;

        /**
         * prediction destructor.
         */
        virtual ~prediction() = default;

        /**
         * Calculates the duration until the first failure.
         *
         * @param results the test results
         * @return the duration until the first failure
         */
        [[nodiscard]] std::uint_fast64_t
        first_failure(const tests::test_results &results) const;
    };
}

#endif /* WEB_PREDICTIONS_PREDICTION_H */
