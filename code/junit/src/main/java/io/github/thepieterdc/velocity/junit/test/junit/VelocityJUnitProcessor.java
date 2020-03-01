/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */

package io.github.thepieterdc.velocity.junit.test.junit;

import io.github.thepieterdc.velocity.junit.test.TestCase;
import org.gradle.api.Action;
import org.gradle.api.internal.tasks.testing.TestClassProcessor;
import org.gradle.api.internal.tasks.testing.TestClassRunInfo;
import org.gradle.api.internal.tasks.testing.TestResultProcessor;
import org.gradle.api.internal.tasks.testing.junit.TestClassExecutionEventGenerator;
import org.gradle.api.internal.tasks.testing.junit.TestClassExecutionListener;
import org.gradle.api.internal.tasks.testing.results.AttachParentTestResultProcessor;
import org.gradle.internal.actor.Actor;
import org.gradle.internal.actor.ActorFactory;
import org.gradle.internal.id.IdGenerator;
import org.gradle.internal.time.Clock;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Custom test processor for JUnit.
 */
public class VelocityJUnitProcessor implements TestClassProcessor {
    private static final Logger LOGGER = LoggerFactory.getLogger(VelocityJUnitProcessor.class);
    
    private final ActorFactory actorFactory;
    private final Clock clock;
    private final IdGenerator<?> idGenerator;
    
    private final TestCase testCase;
    
    private Action<String> executor;
    private Actor resultProcessorActor;
    
    /**
     * VelocityJUnitProcessor constructor.
     *
     * @param testCase     test to execute
     * @param idGenerator  generator for ids
     * @param actorFactory generator for actors
     * @param clock        clock
     */
    public VelocityJUnitProcessor(final TestCase testCase,
                                  final IdGenerator<?> idGenerator,
                                  final ActorFactory actorFactory,
                                  final Clock clock) {
        this.actorFactory = actorFactory;
        this.clock = clock;
        this.idGenerator = idGenerator;
        this.testCase = testCase;
    }
    
    private Action<String> createTestExecutor(final Actor resultProcessorActor) {
        final TestResultProcessor threadSafeResultProcessor = resultProcessorActor.getProxy(TestResultProcessor.class);
        final TestClassExecutionListener threadSafeTestClassListener = resultProcessorActor.getProxy(TestClassExecutionListener.class);
        
        // Create a listener for execution.
        final VelocityJUnitListener listener = new VelocityJUnitListener(
            threadSafeResultProcessor, this.clock, this.idGenerator
        );
        
        return new VelocityJUnitExecutor(
            Thread.currentThread().getContextClassLoader(),
            this.testCase.methodName,
            listener,
            threadSafeTestClassListener
        );
    }
    
    @Override
    public void processTestClass(final TestClassRunInfo testClass) {
        LOGGER.debug("Executing test class {}", testClass.getTestClassName());
        this.executor.execute(testClass.getTestClassName());
    }
    
    @Override
    public void startProcessing(final TestResultProcessor resultProcessor) {
        // Set the result processor.
        this.resultProcessorActor = this.actorFactory.createBlockingActor(
            new TestClassExecutionEventGenerator(
                new AttachParentTestResultProcessor(resultProcessor),
                this.idGenerator,
                this.clock));
        
        // Set the executor.
        this.executor = this.createTestExecutor(this.resultProcessorActor);
    }
    
    @Override
    public void stop() {
        this.resultProcessorActor.stop();
    }
    
    @Override
    public void stopNow() {
        throw new UnsupportedOperationException("stopNow() should not be invoked on remote worker TestClassProcessor");
    }
}
