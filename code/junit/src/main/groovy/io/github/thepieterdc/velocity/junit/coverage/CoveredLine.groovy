/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */
package io.github.thepieterdc.velocity.junit.coverage

/**
 * A covered line.
 */
class CoveredLine {
    final String file
    final int from
    final int to

    /**
     * CoveredLine constructor.
     *
     * @param fileName name of the source file
     * @param fromLine start of the covered block
     * @param toLine end of the covered block
     */
    CoveredLine(final String fileName, final int fromLine, final int toLine) {
        this.file = fileName
        this.from = fromLine
        this.to = toLine
    }

    @Override
    String toString() {
        return String.format('%s [%d - %d]', this.fileName, this.fromLine, this.toLine)
    }
}
