/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */
package io.github.thepieterdc.velocity.junit.tasks

import groovyx.net.http.ContentType
import groovyx.net.http.HTTPBuilder
import groovyx.net.http.Method
import io.github.thepieterdc.velocity.junit.VelocityPluginExtension
import org.gradle.api.DefaultTask
import org.gradle.api.tasks.Input
import org.gradle.api.tasks.TaskAction
import org.slf4j.Logger
import org.slf4j.LoggerFactory

import java.util.function.Consumer
import java.util.function.Supplier

/**
 * Task that creates a new run on a Velocity server.
 */
class VelocityCreateRunTask extends DefaultTask {
    private static final Logger LOG = LoggerFactory.getLogger(VelocityCreateRunTask.class)

    public static final String TASK_NAME = 'velocityCreateRun'

    Supplier<String> commitHashGetter

    Consumer<Long> runIdSetter

    VelocityPluginExtension extension

    @Input
    String server = ""

    @TaskAction
    def create() {
        LOG.info('Creating run.')

        // Create a http client.
        final HTTPBuilder http = new HTTPBuilder(String.format("%s", this.server))
        http.request(Method.POST, ContentType.JSON) {
            uri.path = '/runs'
            body = ['commit_hash': commitHashGetter.get(),
                    'repository' : extension.repository]

            response.success = { final resp, final json ->
                this.runIdSetter.accept(json['id'])
            }

            response.failure = { final resp ->
                throw new RuntimeException(String.valueOf(resp.status))
            }
        }
    }
}
