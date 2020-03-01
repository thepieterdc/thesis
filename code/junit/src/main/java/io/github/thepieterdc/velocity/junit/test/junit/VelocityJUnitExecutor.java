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

import org.gradle.api.Action;
import org.gradle.api.internal.tasks.testing.junit.TestClassExecutionListener;
import org.gradle.internal.concurrent.ThreadSafe;
import org.junit.experimental.runners.Enclosed;
import org.junit.runner.Request;
import org.junit.runner.RunWith;
import org.junit.runner.Runner;
import org.junit.runner.notification.RunListener;
import org.junit.runner.notification.RunNotifier;

public class VelocityJUnitExecutor implements Action<String> {
    private final ClassLoader applicationClassLoader;
    private final TestClassExecutionListener executionListener;
    private final RunListener listener;
    private final String methodName;
    
    /**
     * VelocityJUnitExecutor constructor.
     *
     * @param applicationClassLoader application class loader
     * @param method                 name of the method
     * @param listener               test listener
     * @param executionListener      execution listener
     */
    public VelocityJUnitExecutor(final ClassLoader applicationClassLoader,
                                 final String method,
                                 final RunListener listener,
                                 final TestClassExecutionListener executionListener) {
        assert executionListener instanceof ThreadSafe;
        this.applicationClassLoader = applicationClassLoader;
        this.executionListener = executionListener;
        this.listener = listener;
        this.methodName = method;
    }
    
    @Override
    public void execute(final String testClassName) {
        // Notify the listener.
        this.executionListener.testClassStarted(testClassName);
        
        try {
            // Get an instance of the class to test.
            final Class<?> testClass = Class.forName(
                testClassName,
                false,
                this.applicationClassLoader);
            if (isNestedClassInsideEnclosedRunner(testClass)) {
                return;
            }
            
            // Get a runner for the test method.
            final Request request = Request.method(testClass, this.methodName);
            final Runner runner = request.getRunner();
            
            // Execute the test.
            final RunNotifier notifier = new RunNotifier();
            notifier.addListener(this.listener);
            runner.run(notifier);
    
            // Successful.
            this.executionListener.testClassFinished(null);
        } catch (final Throwable throwable) {
            this.executionListener.testClassFinished(throwable);
        }
    }
    
    // https://github.com/gradle/gradle/issues/2319
    public static boolean isNestedClassInsideEnclosedRunner(Class<?> testClass) {
        if (testClass.getEnclosingClass() == null) {
            return false;
        }
        
        Class<?> outermostClass = testClass;
        while (outermostClass.getEnclosingClass() != null) {
            outermostClass = outermostClass.getEnclosingClass();
        }
        
        RunWith runWith = outermostClass.getAnnotation(RunWith.class);
        return runWith != null && Enclosed.class.equals(runWith.value());
    }
}
