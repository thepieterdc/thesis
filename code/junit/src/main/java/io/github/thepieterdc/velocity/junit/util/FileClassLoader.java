/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */
package io.github.thepieterdc.velocity.junit.util;

import java.io.File;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLClassLoader;
import java.util.Collection;
import java.util.Objects;

/**
 * A class loader consisting of user supplied files.
 */
public final class FileClassLoader {
    /**
     * FileClassLoader constructor.
     */
    private FileClassLoader() {
    
    }
    
    /**
     * Creates the classloader.
     *
     * @param files the files to include
     * @return the classloader
     */
    public static ClassLoader create(final Collection<File> files) {
        final URL[] urls = files.stream()
            .map(File::toURI)
            .map(uri -> {
                try {
                    return uri.toURL();
                } catch (MalformedURLException e) {
                    return null;
                }
            })
            .filter(Objects::nonNull)
            .toArray(URL[]::new);
        return URLClassLoader.newInstance(urls);
    }
}
