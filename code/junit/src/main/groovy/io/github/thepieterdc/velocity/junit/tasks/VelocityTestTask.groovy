/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */
package io.github.thepieterdc.velocity.junit.tasks

import io.github.thepieterdc.velocity.junit.test.TestCase
import io.github.thepieterdc.velocity.junit.test.VelocityTestExecutor
import io.github.thepieterdc.velocity.junit.test.junit.VelocityJUnitFramework
import org.gradle.api.internal.DocumentationRegistry
import org.gradle.api.internal.tasks.testing.JvmTestExecutionSpec
import org.gradle.api.internal.tasks.testing.TestExecuter
import org.gradle.api.internal.tasks.testing.TestFramework
import org.gradle.api.tasks.Input
import org.gradle.api.tasks.TaskAction
import org.gradle.api.tasks.testing.Test
import org.gradle.internal.operations.BuildOperationExecutor
import org.gradle.internal.time.Clock
import org.gradle.internal.work.WorkerLeaseRegistry
import org.gradle.process.JavaForkOptions
import org.gradle.util.RelativePathUtil

import java.util.function.Function

/**
 * Task that runs the tests in the given order.
 */
class VelocityTestTask extends Test {
    public static final String TASK_NAME = "velocity"

    Function<String, File> destinationGenerator = null

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
     * @param testCase the test case
     * @return execution spec
     */
    JvmTestExecutionSpec createTestExecutionSpec(final TestCase testCase) {
        // Create a new Test Framework.
        final TestFramework framework = new VelocityJUnitFramework(this, testCase)

        // Create the execution spec.
        final JavaForkOptions javaForkOptions = this.forkOptionsFactory
            .newJavaForkOptions()
        this.copyTo(javaForkOptions)

        // Get the name of the output file.
        final File outFile = this.destinationGenerator.apply(testCase.flatten())
        final String outFilePath = RelativePathUtil.relativePath(
            this.workingDir,
            outFile
        )

        // Replace the name of the output file in the jvm args.
        javaForkOptions.jvmArgs = Collections.singletonList(javaForkOptions.jvmArgs[0]
            .replace(
                'destfile=',
                String.format('destfile=%s', outFilePath))
            .replace(
                'sessionid=',
                String.format('sessionid=%s', testCase.flatten())
            )
        )

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
