/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */
package io.github.thepieterdc.velocity.junit.example.pkg1;

import org.junit.Assert;
import org.junit.Rule;
import org.junit.Test;
import org.junit.rules.TestRule;
import org.junit.rules.TestWatcher;
import org.junit.runner.Description;

/**
 * Third example test.
 */
public class ThirdTest {
    @Rule
    public TestRule watcher = new TestWatcher() {
        @Override
        protected void starting(final Description description) {
            super.starting(description);
            System.out.println(String.format("Test: ThirdTest#%s", description.getMethodName()));
        }
    };
    
    @Test
    public void testAnotherFoo() {
        Assert.assertEquals(328, HelloAnotherWorld.anotherFoo());
    }
}