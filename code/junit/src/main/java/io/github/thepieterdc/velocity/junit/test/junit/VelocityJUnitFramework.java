/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */

package io.github.thepieterdc.velocity.junit.test.junit;

import io.github.thepieterdc.velocity.junit.test.TestCase;
import org.gradle.api.internal.tasks.testing.TestClassProcessor;
import org.gradle.api.internal.tasks.testing.WorkerTestClassProcessorFactory;
import org.gradle.api.internal.tasks.testing.filter.DefaultTestFilter;
import org.gradle.api.internal.tasks.testing.junit.JUnitTestFramework;
import org.gradle.api.tasks.testing.Test;
import org.gradle.internal.actor.ActorFactory;
import org.gradle.internal.id.IdGenerator;
import org.gradle.internal.service.ServiceRegistry;
import org.gradle.internal.time.Clock;

import java.io.Serializable;

/**
 * Custom test framework for JUnit.
 */
public class VelocityJUnitFramework extends JUnitTestFramework {
    private final TestCase testCase;
    
    /**
     * VelocityFramework constructor.
     *
     * @param testTask the task
     * @param testCase the test case
     */
    public VelocityJUnitFramework(final Test testTask,
                                  final TestCase testCase) {
        super(testTask, new DefaultTestFilter());
        this.testCase = testCase;
    }
    
    @Override
    public WorkerTestClassProcessorFactory getProcessorFactory() {
        return new TestClassProcessorFactoryImpl(this.testCase);
    }
    
    /**
     * Processor factory.
     */
    private static class TestClassProcessorFactoryImpl implements WorkerTestClassProcessorFactory, Serializable {
        private final TestCase testCase;
        
        /**
         * TestClassProcessorFactoryImpl constructor.
         *
         * @param testCase test case to execute
         */
        public TestClassProcessorFactoryImpl(final TestCase testCase) {
            this.testCase = testCase;
        }
        
        @Override
        public TestClassProcessor create(final ServiceRegistry serviceRegistry) {
            return new VelocityJUnitProcessor(
                this.testCase,
                serviceRegistry.get(IdGenerator.class),
                serviceRegistry.get(ActorFactory.class),
                serviceRegistry.get(Clock.class));
        }
    }
}
