/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */
#ifndef WEB_PREDICTIONS_META_PREDICTOR_H
#define WEB_PREDICTIONS_META_PREDICTOR_H

#include "../runs/run.h"
#include "../coverage/manager.h"
#include "manager.h"

namespace predictions {
    /**
     * A meta predictor.
     */
    class meta_predictor {
    private:
        pqxx::connection &db;
        const predictions::manager &predictions;
        const tests::manager &tests;

    public:
        /**
         * meta_predictor constructor.
         *
         * @param db database connection
         * @param predictions predictions manager
         * @param tests tests manager
         */
        explicit meta_predictor(pqxx::connection &db,
                                const predictions::manager &predictions,
                                const tests::manager &tests);

        /**
         * meta_predictor destructor.
         */
        virtual ~meta_predictor() = default;

        /**
         * Updates the predictions for the given run.
         *
         * @param run the run to update
         */
        void update(const runs::run &run) const;
    };
}

#endif /* WEB_PREDICTIONS_META_PREDICTOR_H */
