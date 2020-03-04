/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */
package io.github.thepieterdc.velocity.junit.tasks

import org.gradle.api.DefaultTask
import org.gradle.api.tasks.Input
import org.gradle.api.tasks.TaskAction
import org.jacoco.core.analysis.Analyzer
import org.jacoco.core.analysis.CoverageBuilder
import org.jacoco.core.analysis.IBundleCoverage
import org.jacoco.core.tools.ExecFileLoader
import org.jacoco.report.IReportVisitor
import org.jacoco.report.MultiSourceFileLocator
import org.jacoco.report.xml.XMLFormatter
import org.slf4j.Logger
import org.slf4j.LoggerFactory

import java.util.function.Function

/**
 * Task that parses .exec files to xml.
 */
class VelocityProcessTask extends DefaultTask {
    private static final Logger LOG = LoggerFactory.getLogger(VelocityProcessTask.class)

    public static final String TASK_NAME = 'velocityProcess'

    @Input
    File[] classpath = []

    Function<String, File> destinationGenerator = null

    @Input
    File inputDirectory = null

    @TaskAction
    def parse() {
        LOG.info('Parsing coverage logs.')

        // Find the logs.
        final File[] files = this.inputDirectory
            .listFiles({ final _, final file -> file.endsWith('.exec') } as FilenameFilter)

        // Parse the logs.
        for (final File file : files) {
            this.parseFile(file)
        }

        LOG.info('Parsed all logs.')
    }

    /**
     * Parses a single file.
     *
     * @param file the input file
     */
    private void parseFile(final File file) {
        // Load the execution data.
        final ExecFileLoader loader = new ExecFileLoader()
        loader.load(file)

        // Analyze the execution data.
        final CoverageBuilder builder = new CoverageBuilder()
        final Analyzer analyzer = new Analyzer(loader.executionDataStore, builder)
        for (final File classFile : this.classpath) {
            if (classFile.exists()) {
                analyzer.analyzeAll(classFile)
            }
        }
        final IBundleCoverage coverage = builder.getBundle("Velocity report")

        // Get the xml filename.
        final String outputFileName = file.name.substring(0, file.name.length() - 5)
        final File outputXml = this.destinationGenerator.apply(outputFileName)

        // Write the xml report.
        final IReportVisitor xmlFormatter = new XMLFormatter()
            .createVisitor(new FileOutputStream(outputXml))
        xmlFormatter.visitInfo(loader.sessionInfoStore.infos, loader.executionDataStore.contents)
        xmlFormatter.visitBundle(coverage, new MultiSourceFileLocator(4))
        xmlFormatter.visitEnd()
    }
}
