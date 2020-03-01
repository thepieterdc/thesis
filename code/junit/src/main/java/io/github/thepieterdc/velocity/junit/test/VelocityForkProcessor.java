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
package io.github.thepieterdc.velocity.junit.test;

import org.gradle.api.Action;
import org.gradle.api.internal.DocumentationRegistry;
import org.gradle.api.internal.classpath.ModuleRegistry;
import org.gradle.api.internal.tasks.testing.TestClassProcessor;
import org.gradle.api.internal.tasks.testing.TestClassRunInfo;
import org.gradle.api.internal.tasks.testing.TestResultProcessor;
import org.gradle.api.internal.tasks.testing.WorkerTestClassProcessorFactory;
import org.gradle.api.internal.tasks.testing.worker.RemoteTestClassProcessor;
import org.gradle.api.internal.tasks.testing.worker.TestEventSerializer;
import org.gradle.api.internal.tasks.testing.worker.TestWorker;
import org.gradle.internal.remote.ObjectConnection;
import org.gradle.internal.work.WorkerLeaseRegistry;
import org.gradle.process.JavaForkOptions;
import org.gradle.process.internal.ExecException;
import org.gradle.process.internal.worker.WorkerProcess;
import org.gradle.process.internal.worker.WorkerProcessBuilder;
import org.gradle.process.internal.worker.WorkerProcessFactory;
import org.gradle.util.CollectionUtils;
import org.jacoco.agent.rt.RT;

import java.io.File;
import java.net.URL;
import java.util.List;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

public class VelocityForkProcessor implements TestClassProcessor {
    private final WorkerLeaseRegistry.WorkerLease currentWorkerLease;
    private final WorkerProcessFactory workerFactory;
    private final WorkerTestClassProcessorFactory processorFactory;
    private final JavaForkOptions options;
    private final Iterable<File> classPath;
    private final Action<WorkerProcessBuilder> buildConfigAction;
    private final ModuleRegistry moduleRegistry;
    private final Lock lock = new ReentrantLock();
    private RemoteTestClassProcessor remoteProcessor;
    private WorkerProcess workerProcess;
    private TestResultProcessor resultProcessor;
    private WorkerLeaseRegistry.WorkerLeaseCompletion completion;
    private DocumentationRegistry documentationRegistry;
    private boolean stoppedNow;
    
    /**
     * VelocityForkProcessor constructor.
     *
     * @param parentWorkerLease     worker lease
     * @param workerFactory         factory for workers
     * @param processorFactory      factory for delegates
     * @param options               jvm options
     * @param classPath             tests classpath
     * @param buildConfigAction     configuration task
     * @param moduleRegistry        module registry
     * @param documentationRegistry documentation registry
     */
    public VelocityForkProcessor(final WorkerLeaseRegistry.WorkerLease parentWorkerLease,
                                 final WorkerProcessFactory workerFactory,
                                 final WorkerTestClassProcessorFactory processorFactory,
                                 final JavaForkOptions options,
                                 final Iterable<File> classPath,
                                 final Action<WorkerProcessBuilder> buildConfigAction,
                                 final ModuleRegistry moduleRegistry,
                                 final DocumentationRegistry documentationRegistry) {
        this.currentWorkerLease = parentWorkerLease;
        this.workerFactory = workerFactory;
        this.processorFactory = processorFactory;
        this.options = options;
        this.classPath = classPath;
        this.buildConfigAction = buildConfigAction;
        this.moduleRegistry = moduleRegistry;
        this.documentationRegistry = documentationRegistry;
    }
    
    @Override
    public void startProcessing(TestResultProcessor resultProcessor) {
        this.resultProcessor = resultProcessor;
    }
    
    @Override
    public void processTestClass(TestClassRunInfo testClass) {
        this.lock.lock();
        try {
            if (this.stoppedNow) {
                return;
            }
            
            if (this.remoteProcessor == null) {
                this.completion = this.currentWorkerLease.startChild();
                try {
                    this.remoteProcessor = forkProcess();
                } catch (RuntimeException e) {
                    this.completion.leaseFinish();
                    this.completion = null;
                    throw e;
                }
            }
            
            this.remoteProcessor.processTestClass(testClass);
        } finally {
            this.lock.unlock();
        }
    }
    
    RemoteTestClassProcessor forkProcess() {
        WorkerProcessBuilder builder = this.workerFactory.create(
            new TestWorker(this.processorFactory)
        );
        builder.setBaseName("Velocity Test Executor");
        builder.setImplementationClasspath(getTestWorkerImplementationClasspath());
        builder.applicationClasspath(this.classPath);
        this.options.copyTo(builder.getJavaCommand());
        builder.getJavaCommand().jvmArgs("-Dorg.gradle.native=false");
        this.buildConfigAction.execute(builder);
        
        this.workerProcess = builder.build();
        this.workerProcess.start();
        
        ObjectConnection connection = this.workerProcess.getConnection();
        connection.useParameterSerializers(TestEventSerializer.create());
        connection.addIncoming(TestResultProcessor.class, this.resultProcessor);
        RemoteTestClassProcessor remoteProcessor = connection.addOutgoing(RemoteTestClassProcessor.class);
        connection.connect();
        remoteProcessor.startProcessing();
        return remoteProcessor;
    }
    
    List<URL> getTestWorkerImplementationClasspath() {
        return CollectionUtils.flattenCollections(URL.class,
            this.moduleRegistry.getModule("gradle-core-api").getImplementationClasspath().getAsURLs(),
            this.moduleRegistry.getModule("gradle-worker-processes").getImplementationClasspath().getAsURLs(),
            this.moduleRegistry.getModule("gradle-core").getImplementationClasspath().getAsURLs(),
            this.moduleRegistry.getModule("gradle-logging").getImplementationClasspath().getAsURLs(),
            this.moduleRegistry.getModule("gradle-messaging").getImplementationClasspath().getAsURLs(),
            this.moduleRegistry.getModule("gradle-files").getImplementationClasspath().getAsURLs(),
            this.moduleRegistry.getModule("gradle-hashing").getImplementationClasspath().getAsURLs(),
            this.moduleRegistry.getModule("gradle-base-services").getImplementationClasspath().getAsURLs(),
            this.moduleRegistry.getModule("gradle-cli").getImplementationClasspath().getAsURLs(),
            this.moduleRegistry.getModule("gradle-native").getImplementationClasspath().getAsURLs(),
            this.moduleRegistry.getModule("gradle-testing-base").getImplementationClasspath().getAsURLs(),
            this.moduleRegistry.getModule("gradle-testing-jvm").getImplementationClasspath().getAsURLs(),
            this.moduleRegistry.getModule("gradle-testing-junit-platform").getImplementationClasspath().getAsURLs(),
            this.moduleRegistry.getExternalModule("junit-platform-engine").getImplementationClasspath().getAsURLs(),
            this.moduleRegistry.getExternalModule("junit-platform-launcher").getImplementationClasspath().getAsURLs(),
            this.moduleRegistry.getExternalModule("junit-platform-commons").getImplementationClasspath().getAsURLs(),
            this.moduleRegistry.getModule("gradle-process-services").getImplementationClasspath().getAsURLs(),
            this.moduleRegistry.getExternalModule("slf4j-api").getImplementationClasspath().getAsURLs(),
            this.moduleRegistry.getExternalModule("jul-to-slf4j").getImplementationClasspath().getAsURLs(),
            this.moduleRegistry.getExternalModule("native-platform").getImplementationClasspath().getAsURLs(),
            this.moduleRegistry.getExternalModule("kryo").getImplementationClasspath().getAsURLs(),
            this.moduleRegistry.getExternalModule("commons-lang").getImplementationClasspath().getAsURLs(),
            this.moduleRegistry.getExternalModule("junit").getImplementationClasspath().getAsURLs(),
            RT.class.getProtectionDomain().getCodeSource().getLocation(),
            VelocityForkProcessor.class.getProtectionDomain().getCodeSource().getLocation()
        );
    }
    
    @Override
    public void stop() {
        try {
            if (this.remoteProcessor != null) {
                this.lock.lock();
                try {
                    if (!this.stoppedNow) {
                        this.remoteProcessor.stop();
                    }
                } finally {
                    this.lock.unlock();
                }
                this.workerProcess.waitForStop();
            }
        } catch (ExecException e) {
            if (!this.stoppedNow) {
                throw new ExecException(e.getMessage()
                    + "\nThis problem might be caused by incorrect test process configuration."
                    + "\nPlease refer to the test execution section in the User Manual at "
                    + this.documentationRegistry.getDocumentationFor("java_testing", "sec:test_execution"), e.getCause());
            }
        } finally {
            if (this.completion != null) {
                this.completion.leaseFinish();
            }
        }
    }
    
    @Override
    public void stopNow() {
        this.lock.lock();
        try {
            this.stoppedNow = true;
            if (this.remoteProcessor != null) {
                this.workerProcess.stopNow();
            }
        } finally {
            this.lock.unlock();
        }
    }
}
