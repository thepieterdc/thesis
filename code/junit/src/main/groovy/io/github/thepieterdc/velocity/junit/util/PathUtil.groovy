/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */
package io.github.thepieterdc.velocity.junit.util

/**
 * Utilities for paths.
 */
final class PathUtil {
    /**
     * PathUtil constructor.
     */
    private PathUtil() {

    }

    /**
     * Sanitizes the input path.
     *
     * @param path input
     * @return sanitised path
     */
    static String sanitize(final String path) {
        // Remove trailing slashes and add one.
        return path.replaceAll(/\/+$/, "") + "/"
    }
}
