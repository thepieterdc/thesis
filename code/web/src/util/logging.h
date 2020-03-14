/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */
#ifndef WEB_UTIL_LOGGING_H
#define WEB_UTIL_LOGGING_H

#include <string>
#include <vector>

namespace util::logging {
    /**
     * Logs an error message (varargs).
     *
     * @param fmt the format string or message
     */
    void error(const char *fmt...);

    /**
     * Logs an error message.
     *
     * @param ex the exception to log
     */
    void error(const std::exception &ex);

    /**
     * Logs an error message (varargs) and exits.
     *
     * @param fmt the format string or message
     */
    void fatal(const char *fmt...);

    /**
     * Logs an informational message (varargs).
     *
     * @param fmt the format string or message
     */
    void notice(const char *fmt...);

    /**
     * Logs a success message (varargs).
     *
     * @param fmt the format string or message
     */
    void success(const char *fmt...);
}

#endif /* WEB_UTIL_LOGGING_H */
