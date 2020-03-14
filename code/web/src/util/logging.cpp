/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */

#include <cstdarg>
#include "logging.h"

#define COLOUR_ERROR    "\x1B[1;31m"
#define COLOUR_NOTICE   "\x1B[1;36m"
#define COLOUR_RESET    "\x1B[0m"
#define COLOUR_SUCCESS   "\x1B[1;32m"

#define TYPE_ERROR "ERROR"
#define TYPE_NOTICE "NOTICE"
#define TYPE_SUCCESS "OK"

/**
 * Logs a message to stderr.
 *
 * @param type the type of the message
 * @param message the message format string
 * @param arg_list format arguments
 */
static void log(const char *typemsg, const char *colour, const char *message,
                va_list *arg_list) {
    fprintf(stderr, "%s%-7s%s", colour, typemsg, COLOUR_RESET);
    vfprintf(stderr, message, *arg_list);
    fprintf(stderr, "\n");
}

void util::logging::error(const char *fmt, ...) {
    // Log the message.
    va_list list;
    va_start(list, fmt);
    log(TYPE_ERROR, COLOUR_ERROR, fmt, &list);
    va_end(list);
}

void util::logging::error(const std::exception &ex) {
    error(ex.what());
}

void util::logging::fatal(const char *fmt, ...) {
    // Log the message.
    va_list list;
    va_start(list, fmt);
    log(TYPE_ERROR, COLOUR_ERROR, fmt, &list);
    va_end(list);

    // Exit the program.
    exit(EXIT_FAILURE);
}

void util::logging::notice(const char *fmt, ...) {
    // Log the message.
    va_list list;
    va_start(list, fmt);
    log(TYPE_NOTICE, COLOUR_NOTICE, fmt, &list);
    va_end(list);
}

void util::logging::success(const char *fmt, ...) {
    // Log the message.
    va_list list;
    va_start(list, fmt);
    log(TYPE_SUCCESS, COLOUR_SUCCESS, fmt, &list);
    va_end(list);
}