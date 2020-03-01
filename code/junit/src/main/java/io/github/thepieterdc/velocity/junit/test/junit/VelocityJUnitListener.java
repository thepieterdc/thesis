/*
 * Copyright 2010 the original author or authors.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */
package io.github.thepieterdc.velocity.junit.test.junit;

import org.gradle.api.internal.tasks.testing.DefaultTestDescriptor;
import org.gradle.api.internal.tasks.testing.TestCompleteEvent;
import org.gradle.api.internal.tasks.testing.TestDescriptorInternal;
import org.gradle.api.internal.tasks.testing.TestResultProcessor;
import org.gradle.api.internal.tasks.testing.TestStartEvent;
import org.gradle.api.tasks.testing.TestResult;
import org.gradle.internal.id.IdGenerator;
import org.gradle.internal.time.Clock;
import org.junit.runner.Description;
import org.junit.runner.notification.Failure;
import org.junit.runner.notification.RunListener;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Objects;
import java.util.Set;
import java.util.regex.Pattern;

/**
 * Custom event listener for JUnit. This listener tracks the coverage.
 */
public class VelocityJUnitListener extends RunListener {
    private static final Logger LOG = LoggerFactory.getLogger(VelocityJUnitListener.class);
    
    private static final Pattern DESCRIPTOR_PATTERN = Pattern.compile("(.*)\\((.*)\\)(\\[\\d+])?", Pattern.DOTALL);
    private final IdGenerator<?> idGenerator;
    private final TestResultProcessor resultProcessor;
    private final Clock clock;
    private final Object lock = new Object();
    private final Map<Description, TestDescriptorInternal> executing = new HashMap<>();
    private final Set<Description> assumptionFailed = new HashSet<>();
    
    /**
     * VelocityJUnitListener constructor.
     *
     * @param resultProcessor result processor
     * @param clock           clock
     * @param idGenerator     generator for ids
     */
    public VelocityJUnitListener(final TestResultProcessor resultProcessor,
                                 final Clock clock,
                                 final IdGenerator<?> idGenerator) {
        this.resultProcessor = resultProcessor;
        this.clock = clock;
        this.idGenerator = idGenerator;
    }
    
    @Override
    public void testStarted(Description description) {
        TestDescriptorInternal descriptor = nullSafeDescriptor(this.idGenerator.generateId(), description);
        synchronized (this.lock) {
            TestDescriptorInternal oldTest = this.executing.put(description, descriptor);
            assert oldTest == null : String.format("Unexpected start event for %s", description);
        }
        this.resultProcessor.started(descriptor, this.startEvent());
    }
    
    @Override
    public void testFailure(Failure failure) {
        TestDescriptorInternal descriptor = nullSafeDescriptor(idGenerator.generateId(), failure.getDescription());
        TestDescriptorInternal testInternal;
        synchronized (lock) {
            testInternal = executing.get(failure.getDescription());
        }
        boolean needEndEvent = false;
        if (testInternal == null) {
            // This can happen when, for example, a @BeforeClass or @AfterClass method fails
            needEndEvent = true;
            testInternal = descriptor;
            resultProcessor.started(testInternal, this.startEvent());
        }
        resultProcessor.failure(testInternal.getId(), failure.getException());
        if (needEndEvent) {
            resultProcessor.completed(testInternal.getId(), new TestCompleteEvent(clock.getCurrentTime()));
        }
    }
    
    @Override
    public void testAssumptionFailure(Failure failure) {
        synchronized (lock) {
            assumptionFailed.add(failure.getDescription());
        }
    }
    
    @Override
    public void testFinished(Description description) {
        long endTime = clock.getCurrentTime();
        TestDescriptorInternal testInternal;
        TestResult.ResultType resultType;
        synchronized (lock) {
            testInternal = executing.remove(description);
            if (testInternal == null && executing.size() == 1) {
                // Assume that test has renamed itself (this can actually happen)
                testInternal = executing.values().iterator().next();
                executing.clear();
            }
            assert testInternal != null : String.format("Unexpected end event for %s", description);
            resultType = assumptionFailed.remove(description) ? TestResult.ResultType.SKIPPED : null;
        }
        resultProcessor.completed(testInternal.getId(), new TestCompleteEvent(endTime, resultType));
    }
    
    private TestDescriptorInternal nullSafeDescriptor(final Object id,
                                                      final Description description) {
        final String methodName = Objects.requireNonNullElse(description.getMethodName(), "classMethod");
        return new DefaultTestDescriptor(id, description.getClassName(), methodName);
    }
    
    private TestStartEvent startEvent() {
        return new TestStartEvent(clock.getCurrentTime());
    }
}
