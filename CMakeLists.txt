cmake_minimum_required(VERSION 3.0)
project(TP3 C)
set(CMAKE_C_STANDARD 99)
file(GLOB HEADER_FILES include/*.h )
file(GLOB SOURCE_FILES src/*.c)
set(EXECUTABLE_OUTPUT_PATH ${CMAKE_HOME_DIRECTORY}/bin )
add_executable(TP3 ${HEADER_FILES} ${SOURCE_FILES})
file(COPY ${CMAKE_SOURCE_DIR}/lib/libTP3_provided.dll DESTINATION ${EXECUTABLE_OUTPUT_PATH})
file(COPY ${CMAKE_SOURCE_DIR}/lib/cygTP3_provided.dll DESTINATION ${EXECUTABLE_OUTPUT_PATH})
file(COPY ${CMAKE_SOURCE_DIR}/lib/libTP3_provided.so DESTINATION ${EXECUTABLE_OUTPUT_PATH})
file(COPY ${CMAKE_SOURCE_DIR}/lib/libTP3_provided.dylib DESTINATION ${EXECUTABLE_OUTPUT_PATH})

## if in windows, please comment the one for Ubuntu and MAC OS, and use this instruction.
# for cygwin under windows
# target_link_libraries(TP3 ${CMAKE_SOURCE_DIR}/lib/cygTP3_provided.dll)
# for mingw (GNU GCC) under windows
# target_link_libraries(TP3 ${CMAKE_SOURCE_DIR}/lib/libTP3_provided.dll)
## if in unix-like, e.g, ubuntu, please comment the one for windows and MAC OS, and activate the following instruction.
target_link_libraries(TP3 m ${CMAKE_SOURCE_DIR}/lib/libTP3_provided.so)
## if in MAC OS, please comment the one for windows and ubuntu, and activate the following instruction.
# target_link_libraries(TP3 ${CMAKE_SOURCE_DIR}/lib/libTP3_provided.dylib)
