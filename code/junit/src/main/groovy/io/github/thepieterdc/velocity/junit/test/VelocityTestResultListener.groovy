/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */
package io.github.thepieterdc.velocity.junit.test

import com.fasterxml.jackson.databind.ObjectMapper
import org.gradle.api.tasks.testing.TestDescriptor
import org.gradle.api.tasks.testing.TestListener
import org.gradle.api.tasks.testing.TestResult

/**
 * Listens for the results.
 */
class VelocityTestResultListener implements TestListener {
    private final Map<String, Long> durations
    private final Map<String, Boolean> results

    /**
     * VelocityTestResultListener constructor.
     */
    VelocityTestResultListener() {
        this.durations = new HashMap<>()
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
        this.durations[name] = System.currentTimeMillis()
        this.results[name] = false
    }

    @Override
    void afterTest(final TestDescriptor testDescriptor, final TestResult result) {
        final String name = String.format('%s.%s', testDescriptor.className, testDescriptor.name)
        this.durations[name] = System.currentTimeMillis() - this.durations[name]
        this.results[name] = result.resultType == TestResult.ResultType.SUCCESS
    }

    /**
     * Writes the results to a file.
     *
     * @param output the output file
     */
    void write(final File output) {
        final ObjectMapper mapper = new ObjectMapper()

        // Transform the results to the correct format.
        final Map<String, TestExecution> results = this.results.collectEntries {
            [it.key, new TestExecution(it.value, this.durations[it.key])]
        } as Map<String, TestExecution>

        mapper.writeValue(output, results)
    }
}
