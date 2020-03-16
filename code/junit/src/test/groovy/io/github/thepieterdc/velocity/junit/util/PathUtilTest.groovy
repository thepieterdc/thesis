/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */
package io.github.thepieterdc.velocity.junit.util

import org.junit.Assert
import org.junit.Test

class PathUtilTest extends GroovyTestCase {
    /**
     * Tests PathUtil.sanitize().
     */
    @Test
    void testSanitize() {
        Assert.assertEquals("src/", PathUtil.sanitize("src/"))
        Assert.assertEquals("src/", PathUtil.sanitize("src//"))
        Assert.assertEquals("src/", PathUtil.sanitize("src"))
        Assert.assertEquals("src/main/", PathUtil.sanitize("src/main"))
        Assert.assertEquals("src/main/", PathUtil.sanitize("src/main//"))
        Assert.assertEquals("src/main/", PathUtil.sanitize("src/main/"))
    }
}
