/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */
package io.github.thepieterdc.velocity.junit.test

import org.gradle.api.tasks.testing.TestDescriptor
import org.gradle.api.tasks.testing.TestListener
import org.gradle.api.tasks.testing.TestResult
import com.fasterxml.jackson.databind.ObjectMapper

/**
 * Listens for the results.
 */
class VelocityTestResultListener implements TestListener {
    private final Map<String, Boolean> results;

    /**
     * VelocityTestResultListener constructor.
     */
    VelocityTestResultListener() {
        this.results = new HashMap<>()
    }

    @Override
    void beforeSuite(final TestDescriptor suite) {
        // ignored.
    }

    @Override
    void afterSuite(final TestDescriptor suite, final TestResult result) {
        // ignored.
    }

    @Override
    void beforeTest(final TestDescriptor testDescriptor) {
        // Assume that the test will fail.
        final String name = String.format('%s.%s', testDescriptor.className, testDescriptor.name)
        this.results[name] = false
    }

    @Override
    void afterTest(final TestDescriptor testDescriptor, final TestResult result) {
        final String name = String.format('%s.%s', testDescriptor.className, testDescriptor.name)
        this.results[name] = result.resultType == TestResult.ResultType.SUCCESS
    }

    /**
     * Writes the results to a file.
     *
     * @param output the output file
     */
    void write(final File output) {
        final ObjectMapper mapper = new ObjectMapper()
        mapper.writeValue(output, this.results)
    }
}
