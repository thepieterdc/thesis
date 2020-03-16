/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */
package io.github.thepieterdc.velocity.junit.test


import io.github.thepieterdc.velocity.junit.util.FileClassLoader
import org.gradle.api.internal.tasks.testing.TestClassProcessor
import org.gradle.api.internal.tasks.testing.TestClassRunInfo
import org.gradle.api.internal.tasks.testing.TestResultProcessor
import org.slf4j.Logger
import org.slf4j.LoggerFactory

import java.lang.reflect.Method
import java.util.function.Function
import java.util.stream.Collectors
/**
 * Processes test classes and executes tests.
 */
class VelocityTestProcessor implements TestClassProcessor {
    private static final Logger LOG = LoggerFactory.getLogger(VelocityTestProcessor.class)
    private static final String TEST_ANNOTATION = "org.junit.Test"

    private final Function<TestCase, TestClassProcessor> delegator

    private TestClassProcessor processor
    private boolean stoppedNow

    private final ClassLoader loader
    private TestResultProcessor resultProcessor

    private final List<TestCase> order
    private final Collection<TestCase> tests
    private final Map<String, TestClassRunInfo> testsInfo

    /**
     * VelocityTestProcessor constructor.
     *
     * @param delegator generator for the delegate processor that will execute
     *                  the test
     * @param classpath classpath containing the tests
     * @param orderFile file containing the test order
     */
    VelocityTestProcessor(final Function<TestCase, TestClassProcessor> delegator,
                          final Collection<File> classpath,
                          final List<String> order) {
        this.delegator = delegator
        this.loader = FileClassLoader.create(classpath)
        this.order = VelocityOrderParser.parse(order)
        this.stoppedNow = false
        this.tests = new HashSet<>()
        this.testsInfo = new HashMap<>()
    }

    /**
     * Determines whether the passed method is a test method.
     *
     * @param method the method to test
     * @return true if the method is annotated with @Test
     */
    private static boolean isTest(final Method method) {
        return Arrays.stream(method.annotations)
            .map({ it.annotationType() })
            .map({ it.canonicalName })
            .anyMatch({ final name -> TEST_ANNOTATION == name })
    }

    @Override
    void processTestClass(final TestClassRunInfo testClass) {
        // Create a collection to store the test methods for this class.
        final Collection<String> testMethods = new HashSet<>(10)

        // Load the test class.
        Class<?> cursor = Class.forName(testClass.testClassName, false, this.loader)

        // Consider inheritance.
        while (cursor != Object.class) {
            // Iterate over the methods of the cursor to find @Test-annotated
            // methods.
            testMethods.addAll(Arrays.stream(cursor.methods)
                .filter(VelocityTestProcessor.&isTest)
                .map({ final method -> method.name })
                .collect(Collectors.toSet()))

            // Traverse up the inheritance tree.
            cursor = cursor.superclass
        }

        // Save the test methods.
        testMethods.stream()
            .map({ final method -> new TestCase(testClass.testClassName, method) })
            .forEach(this.tests.&add)
        this.testsInfo[testClass.testClassName] = testClass
    }

    @Override
    void startProcessing(final TestResultProcessor resultProcessor) {
        // Save the result processor.
        this.resultProcessor = resultProcessor

        LOG.info("Parsed order: {} tests.", this.order.size())
    }

    @Override
    void stop() {
        LOG.info("Total tests found: {}.", this.tests.size())

        LOG.info("=============== [Running prioritized tests] ===============")
        for (final TestCase orderedTest : this.order) {
            // Execute the test.
            this.processor = this.delegator.apply(orderedTest)
            this.processor.startProcessing(this.resultProcessor)
            if (this.stoppedNow) {
                return
            }

            this.processor.processTestClass(this.testsInfo[orderedTest.className])
            this.processor.stop()

            // Remove the test from the list of tests.
            this.tests.remove(orderedTest)
        }

        LOG.info("=============== [Running remaining tests] ===============")
        for (final TestCase remainingTest : this.tests) {
            // Execute the test.
            this.processor = this.delegator.apply(remainingTest)
            this.processor.startProcessing(this.resultProcessor)
            if (this.stoppedNow) {
                return
            }
            this.processor.processTestClass(this.testsInfo[remainingTest.className])
            this.processor.stop()
        }
    }

    @Override
    void stopNow() {
        this.stoppedNow = true
        if (this.processor != null) {
            this.processor.stopNow()
        }
    }
}
