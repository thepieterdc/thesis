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

namespace predictions {
    /**
     * A prediction.
     */
    class prediction {
    private:
        const std::string testorder;

        friend class manager;

        /**
         * prediction constructor.
         *
         * @param testorder the predicted order
         */
        explicit prediction(std::string testorder) :
                testorder(std::move(testorder)) {};

    public:
        /**
         * prediction destructor.
         */
        virtual ~prediction() = default;

        /**
         * Gets the order that was predicted.
         *
         * @return the order
         */
        [[nodiscard]] std::list<std::uint_fast64_t> get_order() const;
    };
}

#endif /* WEB_PREDICTIONS_PREDICTION_H */
