# CustomPython OS Platform Configuration
# Detects and configures the build for CustomPython OS target

# Platform detection
if(CMAKE_SYSTEM_NAME STREQUAL "CustomPythonOS")
    set(CUSTOMPYTHON_OS 1)
    set(CUSTOMPYTHON_OS_NAME "CustomPython")
    set(CUSTOMPYTHON_ARCH "x86_64")
else()
    set(CUSTOMPYTHON_OS 0)
    message(STATUS "Building for host system: ${CMAKE_SYSTEM_NAME}")
endif()

# Compiler flags for CustomPython OS
if(CUSTOMPYTHON_OS)
    # Cross-compilation flags
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -ffreestanding -fno-builtin -fno-stack-protector -nostdlib -mcmodel=large")
    set(CMAKE_ASM_FLAGS "${CMAKE_ASM_FLAGS} -felf64")

    # Defines
    add_definitions(
        -DCUSTOMPYTHON_OS=1
        -DCUSTOMPYTHON_OS_NAME="${CUSTOMPYTHON_OS_NAME}"
        -DCUSTOMPYTHON_ARCH="${CUSTOMPYTHON_ARCH}"
        -D_PY_BUILD_CORE
        -D_POSIX_THREADS=1
        -DHAVE_CUSTOMPYTHON_OS=1
    )

    # Feature flags (what the OS supports)
    add_definitions(
        -DHAVE_UNISTD_H=0
        -DHAVE_FCNTL_H=0
        -DHAVE_SIGNAL_H=0
        -DHAVE_DLOPEN=0
        -DHAVE_FORK=0
        -DHAVE_CLOCK_GETTIME=1
        -DHAVE_GETTIMEOFDAY=0
        -DHAVE_SIGACTION=0
        -DHAVE_GETRANDOM=1
        -DHAVE_GETENTROPY=0
        -DHAVE_PIPE2=0
        -DHAVE_VFORK=0
        -DHAVE_LANGINFO_H=0
        -DHAVE_PTHREAD_H=0
    )

    # Disable unsupported modules
    set(DISABLED_MODULES
        _ctypes
        _ssl
        _hashlib
        _socket
        _sqlite3
        readline
        _curses
        _curses_panel
        _tkinter
        _dbm
        _gdbm
        _lzma
        _bz2
        _zstd
        zlib
        _uuid
        _decimal
        _scproxy
    )

    # Platform-specific linker flags
    set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -nostdlib -static -T ${CMAKE_SOURCE_DIR}/os/linker.ld")
endif()

# Define platform-specific types
if(CUSTOMPYTHON_OS)
    set(SIZEOF_VOID_P 8)
    set(SIZEOF_INT 4)
    set(SIZEOF_LONG 8)
    set(SIZEOF_LONG_LONG 8)
    set(SIZEOF_SHORT 2)
    set(SIZEOF_SIZE_T 8)
    set(SIZEOF_PID_T 4)
    set(SIZEOF_OFF_T 8)
    set(SIZEOF_TIME_T 8)
    set(SIZEOF_UID_T 4)
    set(SIZEOF_GID_T 4)
    set(SIZEOF_SIG_ATOMIC_T 4)
endif()
