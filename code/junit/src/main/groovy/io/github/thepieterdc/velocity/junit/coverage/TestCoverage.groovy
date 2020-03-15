/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */
package io.github.thepieterdc.velocity.junit.coverage

/**
 * Coverage data of a test.
 */
class TestCoverage {
    final Collection<CoveredLine> lines
    final String test

    /**
     * TestCoverage constructor.
     *
     * @param testName the name of the test
     */
    TestCoverage(final String testName) {
        this.lines = new HashSet<>(20)
        this.test = testName
    }

    /**
     * Covers the given file lines.
     *
     * @param fileName the file name
     * @param from the start of the coverage block
     * @param to the end of the coverage block
     */
    void cover(final String fileName, final int from, final int to) {
        this.lines.add(new CoveredLine(fileName, from, to))
    }
}
