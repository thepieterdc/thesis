/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */
package io.github.thepieterdc.velocity.junit.test

import io.github.thepieterdc.velocity.junit.util.ImmutableSet
import org.gradle.api.file.FileTree
import org.gradle.api.internal.DocumentationRegistry
import org.gradle.api.internal.classpath.ModuleRegistry
import org.gradle.api.internal.tasks.testing.*
import org.gradle.api.internal.tasks.testing.detection.DefaultTestClassScanner
import org.gradle.api.internal.tasks.testing.detection.TestFrameworkDetector
import org.gradle.api.internal.tasks.testing.processors.TestMainAction
import org.gradle.internal.operations.BuildOperationExecutor
import org.gradle.internal.time.Clock
import org.gradle.internal.work.WorkerLeaseRegistry
import org.gradle.process.internal.worker.WorkerProcessFactory

import java.util.function.Function
/**
 * Executor for tests.
 */
class VelocityTestExecutor implements TestExecuter<JvmTestExecutionSpec> {
    private final BuildOperationExecutor buildOperationExecutor
    private final Clock clock
    private final DocumentationRegistry documentationRegistry
    private final ModuleRegistry moduleRegistry
    private final String orderFile
    private final Function<TestCase, JvmTestExecutionSpec> specGenerator
    private final WorkerProcessFactory workerFactory
    private final WorkerLeaseRegistry workerLeaseRegistry

    private TestClassProcessor processor

    VelocityTestExecutor(final WorkerProcessFactory workerFactory,
                         final ModuleRegistry moduleRegistry,
                         final WorkerLeaseRegistry workerLeaseRegistry,
                         final BuildOperationExecutor buildOperationExecutor,
                         final Clock clock,
                         final DocumentationRegistry documentationRegistry,
                         final Function<TestCase, JvmTestExecutionSpec> specGenerator,
                         final String orderFile) {
        this.buildOperationExecutor = buildOperationExecutor
        this.clock = clock
        this.documentationRegistry = documentationRegistry
        this.moduleRegistry = moduleRegistry
        this.orderFile = orderFile
        this.specGenerator = specGenerator
        this.workerFactory = workerFactory
        this.workerLeaseRegistry = workerLeaseRegistry
    }

    /**
     * Creates a TestProcessor that only executes the given test method.
     *
     * @param testCase the test case to execute
     * @param classpath the classpath
     * @return the processor
     */
    private TestClassProcessor createProcessor(final TestCase testCase,
                                               final Set<? extends File> classpath) {
        // Create an execution spec for the given test method.
        final JvmTestExecutionSpec spec = this.specGenerator.apply(testCase)

        // Create the processor.
        final TestFramework framework = spec.testFramework
        final WorkerLeaseRegistry.WorkerLease worker = this.workerLeaseRegistry
            .currentWorkerLease
        return new VelocityForkProcessor(worker, this.workerFactory,
            framework.processorFactory, spec.javaForkOptions,
            classpath, framework.workerConfigurationAction,
            this.moduleRegistry, this.documentationRegistry)
    }

    @Override
    void execute(final JvmTestExecutionSpec testExecutionSpec, final TestResultProcessor testResultProcessor) {
        final Set<? extends File> classpath = ImmutableSet
            .create(testExecutionSpec.classpath)

        // Create a generator for test processors.
        this.processor = new VelocityTestProcessor({ final method ->
            createProcessor(method, classpath)
        }, classpath, this.orderFile)

        // Create a detector for test files.
        final Runnable detector = this.getDetector(testExecutionSpec, classpath)

        final Object testTaskOperationId = this.buildOperationExecutor
            .currentOperation.parentId

        // Execute all the tests.
        new TestMainAction(detector, this.processor, testResultProcessor,
            this.clock, testTaskOperationId, testExecutionSpec.path,
            "Velocity Test Run " + testExecutionSpec.identityPath).run()
    }

    /**
     * Gets a detector for test files.
     *
     * @param testExecutionSpec specification on which tests to execute
     * @param classpath the classpath containing the tests
     * @return the detector
     */
    private Runnable getDetector(final JvmTestExecutionSpec testExecutionSpec,
                                 final Set<? extends File> classpath) {
        final TestFramework testFramework = testExecutionSpec.testFramework
        final FileTree testClassFiles = testExecutionSpec.candidateClassFiles

        if (!testExecutionSpec.scanForTestClasses || testFramework.detector == null) {
            return new DefaultTestClassScanner(testClassFiles, null, this.processor)
        }

        final TestFrameworkDetector testFrameworkDetector = testFramework.detector
        testFrameworkDetector.testClasses = testExecutionSpec.testClassesDirs.files
        testFrameworkDetector.testClasspath = classpath
        return new DefaultTestClassScanner(testClassFiles, testFrameworkDetector, this.processor)
    }

    @Override
    void stopNow() {
        if (this.processor != null) {
            this.processor.stopNow()
        }
    }
}
