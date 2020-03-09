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

file(GLOB runs_SRC
        "src/runs/*.h"
        "src/runs/*.cpp")

file(GLOB tests_SRC
        "src/tests/*.h"
        "src/tests/*.cpp")

file(GLOB util_SRC
        "src/util/*.h"
        "src/util/*.cpp")

file(GLOB web_SRC
        "src/web/*.h"
        "src/web/*.cpp"
        "src/web/handlers/*.h"
        "src/web/handlers/*.cpp")

# Executables.
add_executable(create-run src/create-run.cpp ${database_SRC} ${runs_SRC} ${util_SRC})
target_link_libraries(create-run sqlite3)

add_executable(get-order src/get-order.cpp ${database_SRC} ${runs_SRC} ${tests_SRC} ${util_SRC})
target_include_directories(get-order PUBLIC ${JSON_INCLUDE_DIRS})
target_link_libraries(get-order sqlite3)

add_executable(parse-coverage src/parse-coverage.cpp ${coverage_SRC} ${database_SRC} ${tests_SRC} ${util_SRC})
target_include_directories(parse-coverage PUBLIC ${JSON_INCLUDE_DIRS} ${ZIPPP_INCLUDE_DIRS})
target_link_libraries(parse-coverage archive pugixml sqlite3 stdc++fs)

add_executable(test-results src/test-results.cpp ${database_SRC} ${tests_SRC} ${util_SRC})
target_include_directories(test-results PUBLIC ${JSON_INCLUDE_DIRS})
target_link_libraries(test-results sqlite3)

add_executable(web src/web.cpp ${coverage_SRC} ${database_SRC} ${runs_SRC} ${tests_SRC} ${util_SRC} ${web_SRC})
target_include_directories(web PUBLIC ${JSON_INCLUDE_DIRS} ${MONGOOSE_INCLUDE_DIRS})
target_link_libraries(web archive ${MONGOOSE_LIBRARIES} pugixml sqlite3 stdc++fs)