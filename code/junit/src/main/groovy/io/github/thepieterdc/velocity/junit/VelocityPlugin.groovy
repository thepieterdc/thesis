/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */
package io.github.thepieterdc.velocity.junit

import io.github.thepieterdc.velocity.junit.coverage.VelocityCoverageAgent
import io.github.thepieterdc.velocity.junit.tasks.*
import org.gradle.api.Plugin
import org.gradle.api.artifacts.Configuration
import org.gradle.api.artifacts.DependencySet
import org.gradle.api.internal.file.FileOperations
import org.gradle.api.internal.project.ProjectInternal
import org.gradle.api.plugins.JavaPluginConvention
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

    private static final String EXTENSION_NAME = 'velocity'

    private static final String COVERAGE_CONFIG = 'velocityCoverageAgent'
    private static final String JACOCO_AGENT = 'org.jacoco:org.jacoco.agent:0.8.5'

    private static final String PROPERTY_COMMIT = 'commit'

    private static final String TASK_ZIP_NAME = 'velocityZip'

    private static final String VELOCITY_DIR = 'velocity'
    private static final String VELOCITY_COVERAGE_FILE = 'test-coverage.json'
    private static final String VELOCITY_COVERAGE_RAW_DIR = 'coverage-raw'
    private static final String VELOCITY_TEST_OUTPUT_FILE = 'test-results.json'

    private static final String VELOCITY_SERVER = 'http://localhost:8080'

    private final Instantiator instantiator
    private ProjectInternal project

    public List<String> order
    public long runId

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

        // Create the extension.
        final VelocityPluginExtension ext = project.extensions
            .create(EXTENSION_NAME, VelocityPluginExtension) as VelocityPluginExtension

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

        // Processed coverage output.
        final File processedCoverageOutputFile = new File(String.format('%s/%s',
            baseDirectory, VELOCITY_COVERAGE_FILE
        ))

        this.configureCreateRunTask(ext)
        this.configureGetOrderTask()
        this.configureTestTask(testOutputFile, coverageOutput)
        this.configureProcessTask(coverageOutput, processedCoverageOutputFile)
        this.configureUploadTask(testOutputFile, processedCoverageOutputFile)

        // Configure the call graph.
        project.tasks
            .findByName(VelocityTestTask.TASK_NAME)
            .finalizedBy(VelocityProcessTask.TASK_NAME)
        project.tasks
            .findByName(VelocityProcessTask.TASK_NAME)
            .finalizedBy(VelocityUploadTask.TASK_NAME)
    }

    /**
     * Configures the create run task.
     *
     * @param ext plugin extension
     * @param commitHash the hash of the current commit
     */
    private void configureCreateRunTask(final VelocityPluginExtension ext) {
        // Add the create run task.
        this.project.tasks.register(
            VelocityCreateRunTask.TASK_NAME,
            VelocityCreateRunTask,
            { final VelocityCreateRunTask task ->
                task.description = 'Creates a new run on a Velocity server.'
                task.group = LifecycleBasePlugin.VERIFICATION_GROUP

                task.commitHashGetter = this.&getCommitHash
                task.extension = ext
                task.runIdSetter = this.&setRunId
                task.server = VELOCITY_SERVER

                task.dependsOn 'cleanTest'
            }
        )
    }

    /**
     * Configures the get order task.
     */
    private void configureGetOrderTask() {
        // Add the create run task.
        this.project.tasks.register(
            VelocityGetOrderTask.TASK_NAME,
            VelocityGetOrderTask,
            { final VelocityGetOrderTask task ->
                task.description = 'Gets the order for the current run.'
                task.group = LifecycleBasePlugin.VERIFICATION_GROUP

                task.orderSetter = this.&setOrder
                task.runIdGetter = this.&getRunId
                task.server = VELOCITY_SERVER

                task.dependsOn VelocityCreateRunTask.TASK_NAME
            }
        )
    }

    /**
     * Configures the process task.
     */
    private void configureProcessTask(final File coverageInput,
                                      final File processedCoverageOutput) {
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
                task.description = 'Parses .exec reports into a json file.'
                task.group = LifecycleBasePlugin.VERIFICATION_GROUP

                task.classpath = outputs
                task.inputDirectory = coverageInput
                task.outputFile = processedCoverageOutput
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
        final JacocoAgentJar agent = this.jacocoAgentJar
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
            VelocityTestTask,
            { final VelocityTestTask task ->
                task.description = 'Executes the tests in a given order.'
                task.group = LifecycleBasePlugin.VERIFICATION_GROUP
                task.jvmArgumentProviders.add(
                    new VelocityCoverageAgent(task, agent)
                )

                task.destinationGenerator = outputCreator
                task.orderGetter = this.&getOrder
                task.results = testOutput

                task.dependsOn VelocityGetOrderTask.TASK_NAME

                LOG.debug(String.format(
                    'Loaded Velocity in %s.',
                    this.project.toString()
                ))
            }
        )
    }

    /**
     * Configures the upload task.
     *
     * @param testResults the json file that contains the test results
     * @param coverageData the json file that contains the coverage data
     */
    private void configureUploadTask(final File testResults,
                                     final File coverageData) {
        // Add the upload task.
        this.project.tasks.register(
            VelocityUploadTask.TASK_NAME,
            VelocityUploadTask.class,
            { final VelocityUploadTask task ->
                task.description = 'Uploads the test results and coverage to the server for analysis'
                task.group = LifecycleBasePlugin.VERIFICATION_GROUP

                task.coverage = coverageData
                task.runIdGetter = this.&getRunId
                task.server = VELOCITY_SERVER
                task.testResults = testResults
            }
        )
    }

    /**
     * Gets the Jacoco agent.
     *
     * @return the agent
     */
    private JacocoAgentJar getJacocoAgentJar() {
        try {
            return this.instantiator.newInstance(
                JacocoAgentJar.class,
                this.project.services.get(FileOperations.class)
            )
        } catch (final Exception ignored) {
            // Fix for old Gradle versions.
            return this.instantiator.newInstance(
                JacocoAgentJar.class,
                this.project
            )
        }
    }

    /**
     * Gets the commit hash from the command line arguments.
     *
     * @return the commit hash
     */
    private String getCommitHash() {
        if (!this.project.hasProperty(PROPERTY_COMMIT)) {
            throw new IllegalArgumentException(
                String.format('Missing required argument: %s', PROPERTY_COMMIT)
            )
        }

        return project[PROPERTY_COMMIT]
    }

    /**
     * Gets the order.
     *
     * @return the order
     */
    private List<String> getOrder() {
        return this.order
    }

    /**
     * Gets the run id.
     *
     * @return the run id
     */
    private long getRunId() {
        return this.runId
    }

    /**
     * Sets the order.
     *
     * @param order the order
     */
    private void setOrder(final List<String> order) {
        this.order = order
    }

    /**
     * Sets the run id.
     *
     * @param id the run id
     */
    private void setRunId(final long id) {
        this.runId = id
    }
}
