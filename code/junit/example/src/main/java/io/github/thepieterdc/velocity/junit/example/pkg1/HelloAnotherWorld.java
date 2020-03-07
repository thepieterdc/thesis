/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */
package io.github.thepieterdc.velocity.junit.example.pkg1;

import io.github.thepieterdc.velocity.junit.example.HelloOtherWorld;

/**
 * Example for the JUnit reorder library.
 */
public class HelloAnotherWorld {
    public static int anotherFoo() {
        final int somebar = HelloOtherWorld.someBar();
        final int resp = somebar * 4;
        return resp;
    }
}
