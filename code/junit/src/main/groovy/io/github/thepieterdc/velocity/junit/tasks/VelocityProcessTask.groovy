/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */
package io.github.thepieterdc.velocity.junit.tasks

import com.fasterxml.jackson.databind.ObjectMapper
import io.github.thepieterdc.velocity.junit.coverage.TestCoverage
import org.gradle.api.DefaultTask
import org.gradle.api.tasks.Input
import org.gradle.api.tasks.TaskAction
import org.jacoco.core.analysis.*
import org.jacoco.core.tools.ExecFileLoader
import org.slf4j.Logger
import org.slf4j.LoggerFactory

/**
 * Task that parses .exec files to xml.
 */
class VelocityProcessTask extends DefaultTask {
    private static final Logger LOG = LoggerFactory.getLogger(VelocityProcessTask.class)

    public static final String TASK_NAME = 'velocityProcess'

    @Input
    File[] classpath = []

    @Input
    File inputDirectory = null

    @Input
    File outputFile = null

    @TaskAction
    def parse() {
        LOG.info('Parsing coverage logs.')

        // Find the logs.
        final File[] files = this.inputDirectory
            .listFiles({ final _, final file -> file.endsWith('.exec') } as FilenameFilter)

        // Parse the logs.
        final Collection<TestCoverage> coverage = new HashSet<>()
        for (final File file : files) {
            coverage.add(this.parseFile(file))
        }

        // Combine the logs into one json file.
        final ObjectMapper mapper = new ObjectMapper()
        mapper.writeValue(this.outputFile, coverage)

        LOG.info('Parsed all logs.')
    }

    /**
     * Parses a single file.
     *
     * @param testOutput the input file
     * @return coverage data for the given test
     */
    private TestCoverage parseFile(final File testOutput) {
        // Load the execution data.
        final ExecFileLoader loader = new ExecFileLoader()
        loader.load(testOutput)

        // Analyze the execution data.
        final CoverageBuilder builder = new CoverageBuilder()
        final Analyzer analyzer = new Analyzer(loader.executionDataStore, builder)
        for (final File classFile : this.classpath) {
            if (classFile.exists()) {
                analyzer.analyzeAll(classFile)
            }
        }
        final IBundleCoverage coverageBundle = builder.getBundle("Velocity report")

        // Create new coverage data.
        final TestCoverage coverage = new TestCoverage(
            loader.sessionInfoStore.infos[0].id
        )

        // Iterate over the packages in the bundle.
        coverageBundle.packages.forEach { final pkg ->
            // Iterate over the source files in the package.
            pkg.sourceFiles.forEach { final source ->
                final String fileName = source.name

                // Iterate over the lines in the file.
                final int lastLine = source.lastLine
                int startBlock = 0
                for (int lineNo = source.firstLine; lineNo <= lastLine; ++lineNo) {
                    final ILine line = source.getLine(lineNo)
                    if (line.status == ICounter.EMPTY || line.status == ICounter.NOT_COVERED) {
                        // The current line is not covered.
                        if (startBlock != 0) {
                            // We were in an ongoing cover block.
                            coverage.cover(fileName, startBlock, lineNo - 1)
                            startBlock = 0
                        }
                    } else if (startBlock == 0) {
                        // Current line is covered and not in an ongoing block.
                        startBlock = lineNo
                    }
                }

                // Close the final block.
                if (startBlock != 0) {
                    coverage.cover(fileName, startBlock, lastLine)
                }
            }
        }

        return coverage
    }
}
