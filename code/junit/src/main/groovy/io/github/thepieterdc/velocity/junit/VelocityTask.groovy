/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */

package io.github.thepieterdc.velocity.junit

import io.github.thepieterdc.velocity.junit.reorder.VelocityTestExecutor
import org.gradle.api.internal.DocumentationRegistry
import org.gradle.api.internal.tasks.testing.JvmTestExecutionSpec
import org.gradle.api.internal.tasks.testing.TestExecuter
import org.gradle.api.internal.tasks.testing.TestFramework
import org.gradle.api.internal.tasks.testing.filter.DefaultTestFilter
import org.gradle.api.internal.tasks.testing.junit.JUnitTestFramework
import org.gradle.api.tasks.Input
import org.gradle.api.tasks.TaskAction
import org.gradle.api.tasks.testing.Test
import org.gradle.internal.operations.BuildOperationExecutor
import org.gradle.internal.time.Clock
import org.gradle.internal.work.WorkerLeaseRegistry
import org.gradle.process.JavaForkOptions

/**
 * Task that runs the tests in the given order.
 */
class VelocityTask extends Test {
    public static final String TASK_NAME = "velocity"

    private TestExecuter<JvmTestExecutionSpec> executor

    @Input
    String orderFile = ""

    @Override
    protected TestExecuter<JvmTestExecutionSpec> createTestExecuter() {
        if (this.executor == null) {
            return new VelocityTestExecutor(this.processBuilderFactory,
                this.moduleRegistry,
                this.services.get(WorkerLeaseRegistry.class) as WorkerLeaseRegistry,
                this.services.get(BuildOperationExecutor.class) as BuildOperationExecutor,
                this.services.get(Clock.class) as Clock,
                this.services.get(DocumentationRegistry.class) as DocumentationRegistry,
                this.&createTestExecutionSpec, this.orderFile)
        } else {
            return this.executor
        }
    }

    /**
     * Creates a TestExecutionSpec for the given test method.
     *
     * @param method test method
     * @return execution spec
     */
    JvmTestExecutionSpec createTestExecutionSpec(final String cls,
                                                 final String method) {
        // Configure the filter.
        final DefaultTestFilter filter = this.instantiator
            .newInstance(DefaultTestFilter.class)
            .includeTest(cls, method) as DefaultTestFilter

        // Create a new Test Framework.
        final TestFramework framework = new JUnitTestFramework(this, filter)

        // Create the execution spec.
        final JavaForkOptions javaForkOptions = this.forkOptionsFactory
            .newJavaForkOptions()
        this.copyTo(javaForkOptions)
        return new JvmTestExecutionSpec(framework, this.classpath,
            this.candidateClassFiles, this.scanForTestClasses,
            this.testClassesDirs, this.path, this.identityPath, this.forkEvery,
            javaForkOptions, this.maxParallelForks, Collections.emptySet())
    }

    @TaskAction
    @Override
    void executeTests() {
        this.testLogging.showStandardStreams = true
        this.executor = this.createTestExecuter()
        super.executeTests()
    }
}
