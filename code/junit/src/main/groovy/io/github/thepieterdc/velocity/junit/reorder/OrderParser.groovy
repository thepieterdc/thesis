/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */
package io.github.thepieterdc.velocity.junit.reorder

import org.gradle.internal.Pair
import org.yaml.snakeyaml.Yaml
import org.yaml.snakeyaml.constructor.Constructor

import java.util.stream.Collectors

/**
 * Parser for order.yaml files.
 */
final class OrderParser {
    static class Order {
        List<Map<String, String>> order = new ArrayList<>()

        List<Map<String, String>> getOrder() {
            return this.order
        }

        void setOrder(final List<Map<String, String>> order) {
            this.order = order
        }
    }

    /**
     * OrderParser constructor.
     */
    private OrderParser() {

    }

    /**
     * Parses the order file.
     *
     * @param file the order file
     * @return the order
     */
    static List<Pair<String, String>> parse(final File file) {
        final Yaml yaml = new Yaml(new Constructor(Order.class))
        final Order parsed = yaml.load(new FileInputStream(file))
        return parsed.order.stream()
            .map({ final item ->
                Pair.of(item['class'], item['method'])
            })
            .collect(Collectors.toList())
    }
}
