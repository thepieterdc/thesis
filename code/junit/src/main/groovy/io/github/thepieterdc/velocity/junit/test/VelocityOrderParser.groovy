/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */
package io.github.thepieterdc.velocity.junit.test

import java.util.stream.Collectors

/**
 * Parser for order json files.
 */
final class VelocityOrderParser {
    /**
     * VelocityOrderParser constructor.
     */
    private VelocityOrderParser() {

    }

    /**
     * Parses the order.
     *
     * @param order the unparsed order
     * @return the order
     */
    static List<TestCase> parse(final List<String> order) {
        return order.stream()
            .map({ final item ->
                final String className = item.substring(0, item.lastIndexOf('.'))
                final String methodName = item.substring(item.lastIndexOf('.') + 1)
                new TestCase(className, methodName)
            })
            .collect(Collectors.toList())
    }
}
