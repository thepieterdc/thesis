/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */
package io.github.thepieterdc.velocity.junit.util

import java.util.stream.Collectors
import java.util.stream.StreamSupport
/**
 * A set of which the contents cannot be modified.
 */
final class ImmutableSet {
    /**
     * ImmutableSet constructor.
     */
    private ImmutableSet() {

    }

    /**
     * Creates an immutable set.
     *
     * @param iterable the iterable to wrap
     * @return the set
     */
    static <T> Set<T> create(final Iterable<T> iterable) {
        return StreamSupport.stream(iterable.spliterator(), false).collect(Collectors.toSet())
    }
}
