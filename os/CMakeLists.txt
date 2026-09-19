# CustomPython OS Kernel Build
# Builds the ASM and C components of the OS kernel

cmake_minimum_required(VERSION 3.20)

# NASM assembler for ASM files
enable_language(ASM_NASM)

# Kernel source files
set(KERNEL_ASM_SOURCES
    boot/boot.asm
    gdt/gdt.asm
    idt/idt.asm
    drivers/vga.asm
    drivers/keyboard.asm
    drivers/timer.asm
    mm/pmm.asm
    mm/vmm.asm
    syscalls/syscall.asm
)

set(KERNEL_C_SOURCES
    kernel.c
    mm/heap.c
    fs/vfs.c
)

# Add ASM flags for NASM
set(CMAKE_ASM_NASM_FLAGS "${CMAKE_ASM_NASM_FLAGS} -f elf64 -g")

# Create kernel object files from ASM
foreach(ASM_SOURCE ${KERNEL_ASM_SOURCES})
    get_filename_component(ASM_NAME ${ASM_SOURCE} NAME_WE)
    add_custom_command(
        OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/${ASM_NAME}.o
        COMMAND nasm -f elf64 -g -o ${CMAKE_CURRENT_BINARY_DIR}/${ASM_NAME}.o
                ${CMAKE_CURRENT_SOURCE_DIR}/${ASM_SOURCE}
        DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/${ASM_SOURCE}
        COMMENT "Assembling ${ASM_SOURCE}"
    )
    list(APPEND KERNEL_OBJECTS ${CMAKE_CURRENT_BINARY_DIR}/${ASM_NAME}.o)
endforeach()

# Create kernel executable
add_executable(custompython-kernel
    ${KERNEL_C_SOURCES}
    ${KERNEL_OBJECTS}
)

# Include directories
target_include_directories(custompython-kernel PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${CMAKE_CURRENT_SOURCE_DIR}/include
)

# Compiler flags
target_compile_options(custompython-kernel PRIVATE
    -ffreestanding
    -fno-builtin
    -fno-stack-protector
    -nostdlib
    -mcmodel=large
    -Wall
    -Wextra
)

# Linker flags
target_link_options(custompython-kernel PRIVATE
    -nostdlib
    -static
    -T ${CMAKE_CURRENT_SOURCE_DIR}/linker.ld
)

# Link dependencies
target_link_libraries(custompython-kernel PRIVATE
    -lgcc
)

# Install
install(TARGETS custompython-kernel RUNTIME DESTINATION bin)
