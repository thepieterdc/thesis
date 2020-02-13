/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */
package io.github.thepieterdc.velocity.junit

import org.gradle.api.Plugin
import org.gradle.api.Project
import org.slf4j.Logger
import org.slf4j.LoggerFactory

/**
 * Main plugin entrypoint.
 */
class VelocityPlugin implements Plugin<Project> {
    private static final Logger LOG = LoggerFactory.getLogger(VelocityPlugin.class)

    @Override
    void apply(final Project project) {
        LOG.debug(String.format("Loaded Velocity in %s.", project.toString()))

        // Add the task.
        final VelocityTask task = project.tasks
            .create(VelocityTask.TASK_NAME, VelocityTask.class)
        task.setDescription("Executes the tests in a given order.")
    }
}
