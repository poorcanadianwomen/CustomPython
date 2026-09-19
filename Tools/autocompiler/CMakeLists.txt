# CustomPython Autocompiler
# Python -> x86-64 ASM transpiler for CustomPython OS

cmake_minimum_required(VERSION 3.20)
project(CustomPythonAutocompiler C)

# The autocompiler itself is written in C (bootstrappable)
# It reads Python source and generates x86-64 assembly for CustomPython OS

set(CMAKE_C_STANDARD 11)

# Autocompiler source files
set(AUTOCOMPILER_SOURCES
    compiler.c
    lexer.c
    parser.c
    codegen.c
    regalloc.c
    optimizer.c
)

# Create autocompiler executable
add_executable(autocompiler
    ${AUTOCOMPILER_SOURCES}
)

target_include_directories(autocompiler PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${CPYTHON_ROOT}/Include
)

# Install
install(TARGETS autocompiler RUNTIME DESTINATION bin)
