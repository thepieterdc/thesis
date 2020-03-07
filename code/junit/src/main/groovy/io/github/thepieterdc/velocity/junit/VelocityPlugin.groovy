/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */
package io.github.thepieterdc.velocity.junit

import io.github.thepieterdc.velocity.junit.coverage.VelocityCoverageAgent
import io.github.thepieterdc.velocity.junit.tasks.VelocityProcessTask
import io.github.thepieterdc.velocity.junit.tasks.VelocityTestTask
import io.github.thepieterdc.velocity.junit.tasks.VelocityUploadTask
import org.gradle.api.Plugin
import org.gradle.api.artifacts.Configuration
import org.gradle.api.artifacts.DependencySet
import org.gradle.api.internal.file.FileOperations
import org.gradle.api.internal.project.ProjectInternal
import org.gradle.api.plugins.JavaPluginConvention
import org.gradle.api.tasks.bundling.Zip
import org.gradle.internal.jacoco.JacocoAgentJar
import org.gradle.internal.reflect.Instantiator
import org.gradle.language.base.plugins.LifecycleBasePlugin
import org.slf4j.Logger
import org.slf4j.LoggerFactory

import javax.inject.Inject
import java.util.function.Function

/**
 * Main plugin entrypoint.
 */
class VelocityPlugin implements Plugin<ProjectInternal> {
    private static final Logger LOG = LoggerFactory.getLogger(VelocityPlugin.class)

    private static final String COVERAGE_CONFIG = 'velocityCoverageAgent'
    private static final String JACOCO_AGENT = 'org.jacoco:org.jacoco.agent:0.8.5'

    private static final String TASK_ZIP_NAME = 'velocityZip'

    private static final String VELOCITY_DIR = 'velocity'
    private static final String VELOCITY_COVERAGE_RAW_DIR = 'coverage-raw'
    private static final String VELOCITY_COVERAGE_DIR = 'coverage'
    private static final String VELOCITY_TEST_OUTPUT_FILE = 'results.json'
    private static final String VELOCITY_ZIP_FILE = 'all.zip'

    private final Instantiator instantiator
    private ProjectInternal project

    /**
     * VelocityPlugin constructor.
     *
     * @param instantiator class instantiator
     */
    @Inject
    VelocityPlugin(final Instantiator instantiator) {
        this.instantiator = instantiator
    }

    @Override
    void apply(final ProjectInternal project) {
        // Save the project.
        this.project = project

        // Set-up the folder structure.
        final FileOperations fileOps = this.project.services
            .get(FileOperations.class) as FileOperations

        final String build = project.layout.buildDirectory.get().asFile
        final String baseDirectory = String.format('%s/%s', build, VELOCITY_DIR)
        fileOps.delete(baseDirectory)
        fileOps.mkdir(baseDirectory)

        // Test output file.
        final File testOutputFile = new File(String.format('%s/%s',
            baseDirectory, VELOCITY_TEST_OUTPUT_FILE
        ))

        // Coverage outputs.
        final File coverageOutput = fileOps.mkdir(String.format('%s/%s',
            baseDirectory, VELOCITY_COVERAGE_RAW_DIR
        ))

        // Processed coverage outputs.
        final File processedCoverageOutput = fileOps.mkdir(String.format('%s/%s',
            baseDirectory, VELOCITY_COVERAGE_DIR
        ))

        // Zip archive.
        final File zipFile = new File(String.format('%s/%s',
            baseDirectory, VELOCITY_ZIP_FILE
        ))

        this.configureTestTask(testOutputFile, coverageOutput)
        this.configureProcessTask(coverageOutput, processedCoverageOutput)
        this.configureZipTask(testOutputFile, processedCoverageOutput, zipFile)
        this.configureUploadTask(zipFile)

        // Configure the call graph.
        project.tasks
            .findByName(VelocityTestTask.TASK_NAME)
            .finalizedBy(VelocityProcessTask.TASK_NAME)
        project.tasks
            .findByName(VelocityProcessTask.TASK_NAME)
            .finalizedBy(TASK_ZIP_NAME)
        project.tasks
            .findByName(TASK_ZIP_NAME)
            .finalizedBy(VelocityUploadTask.TASK_NAME)
    }

    /**
     * Configures the process task.
     */
    private void configureProcessTask(final File coverageInput,
                                      final File processedCoverageOutput) {
        // Create a function that generates output files.
        final Function<String, File> outputCreator = {
            final name -> new File(String.format('%s/%s.xml', processedCoverageOutput.path, name))
        }

        // Get the compiled java output path.
        final File[] outputs = this.project.convention
            .getPlugin(JavaPluginConvention.class)
            .sourceSets
            .findByName('main')
            .output.files

        // Add the report parse task.
        this.project.tasks.register(
            VelocityProcessTask.TASK_NAME,
            VelocityProcessTask.class,
            { final VelocityProcessTask task ->
                task.description = 'Parses .exec reports into .xml'
                task.group = LifecycleBasePlugin.VERIFICATION_GROUP

                task.classpath = outputs
                task.destinationGenerator = outputCreator
                task.inputDirectory = coverageInput
            }
        )
    }

    /**
     * Configures the test task.
     *
     * @param testOutput destination to write the test execution results to
     * @param coverageOutput destination to write the .exec files to
     */
    private void configureTestTask(final File testOutput,
                                   final File coverageOutput) {
        // Create a configuration for the coverage agent.
        final Configuration coverageConfig = project.configurations
            .create(COVERAGE_CONFIG)
        coverageConfig.description = 'Velocity JaCoCo agent.'
        coverageConfig.transitive = true
        coverageConfig.visible = false

        // Create a coverage agent.
        final JacocoAgentJar agent = this.instantiator.newInstance(
            JacocoAgentJar.class,
            this.project.services.get(FileOperations.class)
        )
        agent.agentConf = coverageConfig
        coverageConfig.defaultDependencies({ final DependencySet deps ->
            deps.add(this.project.dependencies.create(JACOCO_AGENT))
        })

        // Create a function that generates output files.
        final Function<String, File> outputCreator = {
            final name -> new File(String.format('%s/%s.exec', coverageOutput.path, name))
        }

        // Add the test task.
        this.project.tasks.register(
            VelocityTestTask.TASK_NAME,
            VelocityTestTask.class,
            { final VelocityTestTask task ->
                task.description = 'Executes the tests in a given order.'
                task.group = LifecycleBasePlugin.VERIFICATION_GROUP
                task.jvmArgumentProviders.add(
                    new VelocityCoverageAgent(task, agent)
                )

                task.destinationGenerator = outputCreator
                task.results = testOutput

                LOG.debug(String.format(
                    'Loaded Velocity in %s.',
                    this.project.toString()
                ))
            }
        )
    }

    /**
     * Configures the upload task.
     */
    private void configureUploadTask(final File zipFile) {
        // Add the zip upload task.
        this.project.tasks.register(
            VelocityUploadTask.TASK_NAME,
            VelocityUploadTask.class,
            { final VelocityUploadTask task ->
                task.description = 'Uploads zip files to the server for analysis'
                task.group = LifecycleBasePlugin.VERIFICATION_GROUP

                task.input = zipFile
            }
        )
    }

    /**
     * Configures the zip task.
     */
    private void configureZipTask(final File testOutput,
                                  final File processedCoverageOutputs,
                                  final File zipFile) {
        // Add the zip task.
        this.project.configure(this.project) {
            task(type: Zip, description: 'Combines the test results and coverage reports into a .zip archive', TASK_ZIP_NAME) {
                archiveName = zipFile
                from(testOutput.parentFile) {
                    include testOutput.name
                }
                from(processedCoverageOutputs) {
                    include '*.xml'
                }
            }
        }
    }
}
