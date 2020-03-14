find_path(MONGOOSE_INCLUDE_DIRS mongoose.h PATHS "${CMAKE_SOURCE_DIR}/lib/mongoose")
find_file(MONGOOSE_LIBRARY mongoose.c PATHS "${CMAKE_SOURCE_DIR}/lib/mongoose")
set(MONGOOSE_LIBRARIES ${MONGOOSE_LIBRARY})