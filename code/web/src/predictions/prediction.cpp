/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */

#include <sstream>
#include "prediction.h"

using prediction = predictions::prediction;

prediction::prediction(std::uint_fast64_t predictor,
                       const std::string &testorder) :
        predictor(predictor) {
    // Parse the order string.
    std::istringstream iss(testorder);
    std::string test_id_str;
    // Iterate over the test ids.
    while (std::getline(iss, test_id_str, ',')) {
        // Parse the id to a number.
        this->testorder.push_back(std::stoi(test_id_str));
    }
}

std::uint_fast64_t
prediction::first_failure(const tests::test_results& results) const {
    uint_fast64_t ret = 0;
    for (const auto &it : this->testorder) {
        const auto& result = results.at(it);
        if (result->failed) {
            return ret;
        }
        ret += result->duration;
    }

    return ret;
}