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

import java.util.function.Supplier
/**
 * Task that uploads zip file to the server for analysis.
 */
class VelocityUploadTask extends DefaultTask {
    private static final Logger LOG = LoggerFactory.getLogger(VelocityUploadTask.class)

    public static final String TASK_NAME = 'velocityUpload'

    @Input
    File coverage = null

    VelocityPluginExtension extension

    Supplier<Long> runIdGetter

    @Input
    String server = ""

    @Input
    File testResults = null

    @TaskAction
    def parse() {
        LOG.info('Uploading test results.')

        // Upload the test results.
        HTTPBuilder http = new HTTPBuilder(extension.server)
        http.request(Method.POST, ContentType.JSON) {
            uri.path = String.format('/runs/%d/test-results', this.runIdGetter.get())
            body = this.testResults.text

            response.failure = { final resp ->
                throw new RuntimeException(String.valueOf(resp.status))
            }
        }

        LOG.info('Test results uploaded.')

        LOG.info('Uploading coverage logs.')

        // Upload the coverage logs.
        http = new HTTPBuilder(String.format("%s", this.server))
        http.request(Method.POST, ContentType.JSON ) { final request ->
            uri.path = String.format('/runs/%d/coverage', this.runIdGetter.get())
            body = this.coverage.text

            response.failure = { final resp ->
                throw new RuntimeException(String.valueOf(resp.status))
            }
        }

        LOG.info('Coverage logs uploaded.')
    }
}
