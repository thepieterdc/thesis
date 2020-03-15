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
find_package(Mongoose REQUIRED)

# Files.
file(GLOB coverage_SRC
        "src/coverage/*.h"
        "src/coverage/*.cpp")

file(GLOB database_SRC
        "src/database/*.h"
        "src/database/*.cpp")

file(GLOB repositories_SRC
        "src/repositories/*.h"
        "src/repositories/*.cpp")

file(GLOB runs_SRC
        "src/runs/*.h"
        "src/runs/*.cpp")

file(GLOB server_SRC
        "src/server/*.h"
        "src/server/*.cpp"
        "src/server/handlers/*.h"
        "src/server/handlers/*.cpp")

file(GLOB tests_SRC
        "src/tests/*.h"
        "src/tests/*.cpp")

file(GLOB util_SRC
        "src/util/*.h"
        "src/util/*.cpp")

# Executables.
add_executable(create-run src/create-run.cpp ${database_SRC} ${repositories_SRC} ${runs_SRC} ${util_SRC})
target_link_libraries(create-run pqxx)

add_executable(get-order src/get-order.cpp ${database_SRC} ${runs_SRC} ${tests_SRC} ${util_SRC})
target_include_directories(get-order PUBLIC ${JSON_INCLUDE_DIRS})
target_link_libraries(get-order pqxx)

add_executable(server src/server.cpp ${coverage_SRC} ${database_SRC} ${repositories_SRC} ${runs_SRC} ${server_SRC} ${tests_SRC} ${util_SRC})
target_include_directories(server PUBLIC ${JSON_INCLUDE_DIRS} ${MONGOOSE_INCLUDE_DIRS})
target_link_libraries(server ${MONGOOSE_LIBRARIES} pqxx)

add_executable(test-coverage src/test-coverage.cpp ${coverage_SRC} ${database_SRC} ${tests_SRC} ${util_SRC})
target_include_directories(test-coverage PUBLIC ${JSON_INCLUDE_DIRS} ${ZIPPP_INCLUDE_DIRS})
target_link_libraries(test-coverage pqxx)

add_executable(test-results src/test-results.cpp ${database_SRC} ${runs_SRC} ${tests_SRC} ${util_SRC})
target_include_directories(test-results PUBLIC ${JSON_INCLUDE_DIRS})
target_link_libraries(test-results pqxx)