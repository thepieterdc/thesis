/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */
package io.github.thepieterdc.velocity.junit.example;

import org.junit.Assert;
import org.junit.Rule;
import org.junit.Test;
import org.junit.rules.TestRule;
import org.junit.rules.TestWatcher;
import org.junit.runner.Description;

/**
 * First example test.
 */
public class FirstTest {
    @Rule
    public TestRule watcher = new TestWatcher() {
        @Override
        protected void starting(final Description description) {
            super.starting(description);
            System.out.println(String.format("Test: FirstTest#%s", description.getMethodName()));
        }
    };
    
    @Test
    public void testFoo() {
        Assert.assertFalse(HelloWorld.foo());
    }
    
    @Test
    public void testHello() {
        Assert.assertEquals("Hello", HelloWorld.hello());
    }
}