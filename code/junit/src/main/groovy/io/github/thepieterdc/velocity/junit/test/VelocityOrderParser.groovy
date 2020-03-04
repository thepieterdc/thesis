/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */
package io.github.thepieterdc.velocity.junit.test


import org.yaml.snakeyaml.Yaml
import org.yaml.snakeyaml.constructor.Constructor

import java.util.stream.Collectors

/**
 * Parser for order.yaml files.
 */
final class VelocityOrderParser {
    static class Order {
        List<String> order = new ArrayList<>()

        List<String> getOrder() {
            return this.order
        }

        void setOrder(final List<String> order) {
            this.order = order
        }
    }

    /**
     * OrderParser constructor.
     */
    private VelocityOrderParser() {

    }

    /**
     * Parses the order file.
     *
     * @param file the order file
     * @return the order
     */
    static List<TestCase> parse(final File file) {
        final Yaml yaml = new Yaml(new Constructor(Order.class))
        final Order parsed = yaml.load(new FileInputStream(file))
        return parsed.order.stream()
            .map({ final item ->
                final String className = item.substring(0, item.lastIndexOf('.'))
                final String methodName = item.substring(item.lastIndexOf('.') + 1)
                new TestCase(className, methodName)
            })
            .collect(Collectors.toList())
    }
}
