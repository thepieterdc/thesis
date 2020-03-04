/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */
package io.github.thepieterdc.velocity.junit.tasks

import groovyx.net.http.HTTPBuilder
import groovyx.net.http.Method
import org.apache.http.entity.ContentType
import org.apache.http.entity.mime.MultipartEntityBuilder
import org.gradle.api.DefaultTask
import org.gradle.api.tasks.Input
import org.gradle.api.tasks.TaskAction
import org.slf4j.Logger
import org.slf4j.LoggerFactory

import static groovyx.net.http.ContentType.JSON

/**
 * Task that uploads zip file to the server for analysis.
 */
class VelocityUploadTask extends DefaultTask {
    private static final Logger LOG = LoggerFactory.getLogger(VelocityUploadTask.class)

    public static final String TASK_NAME = 'velocityUpload'

    @Input
    File input = null

    @TaskAction
    def parse() {
        LOG.info('Uploading coverage archive.')

        // Create a http client.
        final HTTPBuilder http = new HTTPBuilder('http://localhost:8080/evaluate')
        http.request(Method.POST, JSON) { final request ->
            headers.'Accept' = 'application/json'

            final MultipartEntityBuilder entityBuilder = MultipartEntityBuilder
                .create()
                .addBinaryBody('file', this.input, ContentType.DEFAULT_BINARY, this.input.name)

            request.entity = entityBuilder.build()
        }
    }
}
