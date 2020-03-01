/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */
package io.github.thepieterdc.velocity.junit.coverage

import io.github.thepieterdc.velocity.junit.tasks.VelocityTestTask
import org.gradle.internal.jacoco.JacocoAgentJar
import org.gradle.process.CommandLineArgumentProvider
import org.gradle.process.JavaForkOptions
import org.gradle.util.RelativePathUtil

class VelocityCoverageAgent implements CommandLineArgumentProvider {
    private final JacocoAgentJar agent
    private final JavaForkOptions task

    /**
     * VelocityCoverageAgent constructor.
     *
     * @param task task
     * @param agent jacoco agent to attach
     */
    VelocityCoverageAgent(final VelocityTestTask task,
                          final JacocoAgentJar agent) {
        this.agent = agent
        this.task = task
    }

    @Override
    Iterable<String> asArguments() {
        // Get the path to the JaCoCo agent.
        final String agentPath = RelativePathUtil.relativePath(
            this.task.workingDir,
            this.agent.jar
        )

        // Build the argument string.
        final StringBuilder builder = new StringBuilder();
        builder.append('-javaagent:')
        builder.append(agentPath)
        builder.append('=')
        builder.append('append=false,')
        builder.append('destfile=,')
        builder.append('sessionid=,')
        builder.append('dumponexit=true')

        // Get the argument as a list.
        return Arrays.asList(builder.toString())
    }
}
