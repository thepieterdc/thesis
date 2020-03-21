/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */

#include <sstream>
#include "prediction.h"

std::list<std::uint_fast64_t> predictions::prediction::get_order() const {
    // Create a new list.
    std::list<std::uint_fast64_t> order;

    // Parse the order string.
    std::istringstream iss(this->testorder);
    std::string test_id_str;
    // Iterate over the test ids.
    while (std::getline(iss, test_id_str, ',')) {
        // Parse the id to a number.
        order.push_back(std::stoi(test_id_str));
    }

    // Return the parsed order.
    return order;
}