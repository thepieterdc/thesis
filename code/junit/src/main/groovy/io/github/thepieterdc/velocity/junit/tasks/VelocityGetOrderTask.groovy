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
class VelocityGetOrderTask extends DefaultTask {
    private static final Logger LOG = LoggerFactory.getLogger(VelocityGetOrderTask.class)

    public static final String TASK_NAME = 'velocityGetOrder'

    Consumer<List<String>> orderSetter

    Supplier<Long> runIdGetter

    @Input
    String server = ""

    @TaskAction
    def parse() {
        LOG.info('Getting the order.')

        // Get the order.
        boolean found = false

        while (!found) {
            final HTTPBuilder http = new HTTPBuilder(String.format("%s", this.server))
            http.request(Method.GET, ContentType.JSON) {
                uri.path = String.format('/runs/%d', this.runIdGetter.get())

                response.failure = { final resp ->
                    throw new Exception(String.valueOf(resp.status))
                }

                response.success = { final resp, final json ->
                    if (resp.status == 200) {
                        found = true
                        orderSetter.accept(json['order'])
                    }
                }
            }

            // Delay to retry.
            Thread.sleep(5000L)
        }
    }
}
