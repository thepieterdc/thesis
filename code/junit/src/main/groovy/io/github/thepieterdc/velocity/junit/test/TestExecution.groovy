/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */

package io.github.thepieterdc.velocity.junit.test

/**
 * The result of a test execution.
 */
class TestExecution {
    public long duration
    public boolean result

    /**
     * TestExecution constructor.
     *
     * @param result result of the test
     * @param duration duration of the test
     */
    TestExecution(final boolean result, final long duration) {
        this.duration = duration
        this.result = result
    }
}
