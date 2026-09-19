cmake_minimum_required(VERSION 3.20)
project(CustomPython C ASM)

# CustomPython OS + CPython Fork
# Builds the OS kernel and CPython interpreter for CustomPython OS

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)

# Build options
option(CUSTOMPYTHON_BUILD_KERNEL "Build CustomPython OS kernel" ON)
option(CUSTOMPYTHON_BUILD_INTERPRETER "Build CPython interpreter" ON)
option(CUSTOMPYTHON_BUILD_AUTOCOMPILER "Build Python->ASM autocompiler" ON)
option(CUSTOMPYTHON_STATIC_BUILD "Static build (no shared libraries)" ON)
option(CUSTOMPYTHON_DEBUG "Debug build with symbols" OFF)

# Set output directories
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)

# Include custom modules
list(APPEND CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/cmake")

# Include platform configuration
include(cmake/CustomPythonOS.cmake)

# Subdirectories
if(CUSTOMPYTHON_BUILD_KERNEL)
    add_subdirectory(os)
endif()

if(CUSTOMPYTHON_BUILD_INTERPRETER)
    # The CPython source is in the root of this project
    # We add it as a subdirectory with our custom CMakeLists
    add_subdirectory(Platform/CustomPython)
endif()

if(CUSTOMPYTHON_BUILD_AUTOCOMPILER)
    add_subdirectory(Tools/autocompiler)
endif()

# Install targets
install(DIRECTORY os/bin DESTINATION share/custompython/bin OPTIONAL)
install(DIRECTORY Lib/ DESTINATION share/custompython/lib)
install(DIRECTORY Platform/CustomPython DESTINATION share/custompython/platform)
