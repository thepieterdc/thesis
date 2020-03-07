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
 * Second example test.
 */
public class SecondTest {
    @Rule
    public TestRule watcher = new TestWatcher() {
        @Override
        protected void starting(final Description description) {
            super.starting(description);
            System.out.println(String.format("Test: SecondTest#%s", description.getMethodName()));
        }
    };
    
    @Test
    public void testUnlisted() {
        Assert.assertTrue(HelloWorld.unlisted());
    }
    
    @Test
    public void testBar() {
        Assert.assertEquals(42, HelloWorld.bar());
    }
    
    @Test
    public void testLoremIpsum() {
        Assert.assertEquals("Lorem ipsum dolor sit amet consectetur adipiscing elit.", HelloWorld.loremIpsum());
    }
    
    @Test
    public void testOtherBar() {
        Assert.assertEquals(84, HelloOtherWorld.someBar());
    }
    
    @Test
    public void testWorld() {
        Assert.assertEquals("World", HelloWorld.world());
    }
}