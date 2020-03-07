cmake_minimum_required(VERSION 3.10.2)
project(analyser)

# Build type.
if (NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Debug)
endif ()

message("Build type: ${CMAKE_BUILD_TYPE}")

# Configure extra modules.
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_SOURCE_DIR}/cmake")

# Compilation flags.
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} --std=c++17")
set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -O0 -ggdb")
set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -O3 -s")
add_compile_options(-Wall -Wextra -Wpedantic -Wno-missing-field-initializers -Wno-unused-parameter)

# Packages.
find_package(Json REQUIRED)

# Files.
file(GLOB coverage_SRC
        "src/coverage/*.h"
        "src/coverage/*.cpp")

file(GLOB database_SRC
        "src/database/*.h"
        "src/database/*.cpp")

file(GLOB runs_SRC
        "src/runs/*.h"
        "src/runs/*.cpp")

file(GLOB tests_SRC
        "src/tests/*.h"
        "src/tests/*.cpp")

# Executables.
add_executable(analyser main.cpp ${coverage_SRC} ${database_SRC} ${runs_SRC} ${tests_SRC})
target_link_libraries(analyser pugixml stdc++fs sqlite3)
include_directories(${JSON_INCLUDE_DIRS})