/*
 * Copyright (c) 2019-2020. All rights reserved.
 *
 * @author Pieter De Clercq
 *
 * https://github.com/thepieterdc/thesis/
 */

#include <experimental/filesystem>
#include <iostream>
#include <pugixml.hpp>
#include "manager.h"
#include "buffer.h"

namespace fs = std::experimental::filesystem;

bool coverage::manager::available(const std::uint_fast64_t test_id) const {
    const std::string sql(
            "SELECT COUNT(1) FROM tests_coverage WHERE test_id=?"
    );
    const auto stmt = this->db.prepare(sql);
    stmt->bind_integer(1, test_id);
    const auto found = database::connection::find(*stmt);

    // Validate the result of the query.
    return found && stmt->get_integer(0) > 0;
}

void coverage::manager::clear(const std::uint_fast64_t test_id) const {
    const std::string sql("DELETE FROM tests_coverage WHERE test_id=?");
    const auto stmt = this->db.prepare(sql);
    stmt->bind_integer(1, test_id);
    database::connection::exec(*stmt);
}

void coverage::manager::parse(const runs::run &run,
                              const std::string &file) const {
    // Open the xml file.
    pugi::xml_document doc;
    if (!doc.load_file(file.c_str())) {
        throw std::runtime_error("Failed parsing xml.");
    }

    // Get the name of the test case.
    const auto *const testcase = doc.child("report")
            .child("sessioninfo").attribute("id").value();

    // Get the id of the test case.
    const auto opt_result = this->tests.find_result(run, testcase);
    if (!opt_result.has_value()) {
        throw std::runtime_error("Test result not found.");
    }
    const auto &result = opt_result.value();

    // Find whether the coverage for this test should be saved.
    if (this->available(result->test_id) && result->failed) {
        // Coverage for this test is already available, however the test did not
        // reach the end, so the updated coverage may possibly not represent the
        // actual test coverage.
        return;
    }

    // Delete the current test coverage information for this test.
    this->clear(result->test_id);

    // Iterate over the packages.
    for (const auto &package : doc.child("report").children("package")) {
        // Get the name of the folder.
        const std::string package_name = package.attribute("name").value();

        // Iterate over the source files.
        for (const auto &source_file : package.children("sourcefile")) {
            // Get the name of the file.
            const std::string file_name = source_file.attribute("name").value();
            // Get the full path.
            const auto full_path = std::string(package_name) + "/" + file_name;

            // Create a buffer to handle coverage data.
            coverage::buffer buffer(this->db, full_path, result->test_id);

            // Iterate over the source lines.
            for (const auto &line : source_file.children("line")) {
                // Get the line no.
                uint_fast32_t line_no = line.attribute("nr").as_int();
                // Get whether the line is covered.
                bool line_covered = line.attribute("ci").as_int() > 0;

                if (line_covered) {
                    // Add the covered line.
                    buffer.cover(line_no);
                }
            }

            // Flush the buffer.
            buffer.flush();
        }
    }
}

void coverage::manager::parse_all(const runs::run &run,
                                  const std::string &path) const {
    // Iterate over every file in the directory.
    for (const auto &file : fs::directory_iterator(path)) {
        const auto &file_path = file.path();

        // Only consider xml files.
        if (file_path.extension().string() != ".xml") {
            continue;
        }

        // Parse the file.
        this->parse(run, file_path);
    }
}