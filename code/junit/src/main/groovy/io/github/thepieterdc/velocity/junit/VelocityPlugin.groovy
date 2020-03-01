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
import java.nio.file.Paths
import java.util.function.Function

/**
 * Main plugin entrypoint.
 */
class VelocityPlugin implements Plugin<ProjectInternal> {
    private static final Logger LOG = LoggerFactory.getLogger(VelocityPlugin.class)

    private static final String COVERAGE_CONFIG = 'velocityCoverageAgent'
    private static final String JACOCO_AGENT = 'org.jacoco:org.jacoco.agent:0.8.5'

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

        // Create required folder structure.
        final FileOperations fileOps = this.project.services
            .get(FileOperations.class) as FileOperations

        // Coverage outputs.
        final String coverageOutputFolder = String.format("%s/coverage/",
            project.layout.buildDirectory.get().asFile
        )
        final File coverageOutput = this.project.providers
            .provider({ fileOps.mkdir(coverageOutputFolder) })
            .get()

        // Processed coverage outputs.
        final String processedCoverageOutputFolder = String.format("%s/coverage-processed/",
            project.layout.buildDirectory.get().asFile
        )
        final File processedCoverageOutput = this.project.providers
            .provider({ fileOps.mkdir(processedCoverageOutputFolder) })
            .get()

        this.configureTestTask(coverageOutput)
        this.configureProcessTask(coverageOutput, processedCoverageOutput)

        // Configure the call graph.
        project.tasks
            .findByName(VelocityTestTask.TASK_NAME)
            .finalizedBy(VelocityProcessTask.TASK_NAME)
    }

    /**
     * Configures the process task.
     */
    private void configureProcessTask(final File coverageInput,
                                      final File processedCoverageOutput) {
        // Create a function that generates output files.
        final Function<String, File> outputCreator = {
            final name ->
                this.project.providers
                    .provider({ Paths.get(processedCoverageOutput.path, String.format("%s.xml", name)) })
                    .get()
                    .toFile()
        }

        // Get the compiled java output path.
        final File[] outputs = project.convention
            .getPlugin(JavaPluginConvention.class)
            .sourceSets
            .findByName('main')
            .output.files

        // Add the report parse task.
        project.tasks.register(
            VelocityProcessTask.TASK_NAME,
            VelocityProcessTask.class,
            { final VelocityProcessTask task ->
                task.description = 'Parses .exec reports into .xml'
                task.group = LifecycleBasePlugin.VERIFICATION_GROUP

                task.classpath = outputs

                task.inputDirectory = coverageInput
                task.destinationGenerator = outputCreator
            }
        )
    }

    /**
     * Configures the test task.
     *
     * @param coverageOutput destination to write the .exec files to
     */
    private void configureTestTask(final File coverageOutput) {
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
            final name ->
                this.project.providers
                    .provider({ Paths.get(coverageOutput.path, String.format("%s.exec", name)) })
                    .get()
                    .toFile()
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

                LOG.debug(String.format(
                    'Loaded Velocity in %s.',
                    this.project.toString()
                ))
            }
        )
    }
}
