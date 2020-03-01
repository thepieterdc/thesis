/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */
package io.github.thepieterdc.velocity.junit.test;

import java.io.Serializable;
import java.util.Objects;

/**
 * A test case.
 */
public final class TestCase implements Serializable {
    public final String className;
    public final String methodName;
    
    /**
     * TestCase constructor.
     *
     * @param className  name of the class
     * @param methodName name of the method
     */
    public TestCase(final String className, final String methodName) {
        this.className = className;
        this.methodName = methodName;
    }
    
    @Override
    public boolean equals(final Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        final TestCase testCase = (TestCase) o;
        return Objects.equals(this.className, testCase.className) &&
            Objects.equals(this.methodName, testCase.methodName);
    }
    
    @Override
    public int hashCode() {
        return Objects.hash(this.className, this.methodName);
    }
    
    public String flatten() {
        return String.format("%s.%s", this.className, this.methodName);
    }
}
