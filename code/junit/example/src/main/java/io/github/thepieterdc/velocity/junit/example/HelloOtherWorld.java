/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */
package io.github.thepieterdc.velocity.junit.example;

/**
 * Example for the JUnit reorder library.
 */
public class HelloOtherWorld {
    public static int someBar() {
        return HelloWorld.bar() * 2;
    }
}
