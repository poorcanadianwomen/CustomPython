# CustomPython

A custom fork of CPython 3.16.0a0 with an x86-64 ASM operating system, CMake build system, and Python-to-ASM autocompiler.

## Architecture

```
CustomPython/
├── os/                    # x86-64 ASM OS Kernel
│   ├── boot/              # Bootloader (Multiboot2, long mode)
│   ├── drivers/           # VGA, keyboard, timer
│   ├── gdt/               # Global Descriptor Table
│   ├── idt/               # Interrupt Descriptor Table
│   ├── mm/                # Memory management (PMM, VMM, heap)
│   ├── fs/                # Virtual filesystem
│   ├── syscalls/          # System call interface
│   └── kernel.c           # Main kernel entry point
├── Include/cpythonos/     # CustomPython OS pyconfig.h
├── Lib/cpythonos/         # Python OS interface module
├── Platform/CustomPython/ # CPython fork configuration
├── Tools/
│   ├── autocompiler/      # Python -> x86-64 ASM transpiler
│   └── pkgmanager/        # Package manager
├── cmake/                 # CMake modules
└── CMakeLists.txt         # Top-level CMake build
```

## Requirements

- **Linux** (or WSL2 on Windows)
- **CMake** >= 3.20
- **NASM** (Netwide Assembler)
- **GCC** (cross-compiler or native)
- **GRUB** (for ISO creation)
- **QEMU** (for testing)

Install on Ubuntu/Debian:
```bash
sudo apt install cmake nasm gcc grub-pc-bin grub-common xorriso mtools qemu-system-x86
```

## Building

### Quick Build
```bash
chmod +x build.sh
./build.sh
```

### Manual Build
```bash
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
cmake --build . -j$(nproc)
```

### Create Bootable ISO
```bash
chmod +x tools/create_iso.sh
./tools/create_iso.sh
```

### Run in QEMU
```bash
chmod +x tools/run_qemu.sh
./tools/run_qemu.sh
```

## Features

### ASM OS Kernel
- Multiboot2-compliant bootloader
- 64-bit long mode with page tables
- Physical memory manager (bitmap allocator)
- Virtual memory manager
- Heap allocator (for CPython's malloc/free)
- PS/2 keyboard driver
- PIT timer driver
- VGA text-mode output
- System call interface (27 syscalls)
- Virtual filesystem abstraction

### CPython Fork
- CPython 3.16.0a0 core
- CMake build system (replaces autoconf/make)
- Custom Python modules:
  - `_cpythonos` - OS interface via syscalls
  - `os` - Standard library os module
- Static linking (no shared libraries)
- Reduced standard library (no network, no SSL, no ctypes)

### Autocompiler (WIP)
- Python -> x86-64 ASM transpiler
- Generates ELF binaries for CustomPython OS
- Bootstrappable (written in C)

## Syscall Interface

| # | Name | Description |
|---|------|-------------|
| 0 | sys_exit | Terminate process |
| 1 | sys_read | Read from file descriptor |
| 2 | sys_write | Write to file descriptor |
| 3 | sys_open | Open file |
| 4 | sys_close | Close file descriptor |
| 5 | sys_fstat | Get file status |
| 6 | sys_mmap | Memory map |
| 7 | sys_munmap | Unmap memory |
| 8 | sys_brk | Change heap size |
| 9 | sys_nanosleep | Sleep |
| 10 | sys_clock_gettime | Get time |
| 11 | sys_getcwd | Get current directory |
| 12 | sys_chdir | Change directory |
| 13 | sys_stat | File stat |
| 14 | sys_dup | Duplicate fd |
| 15 | sys_dup2 | Duplicate fd to specific number |
| 16 | sys_pipe | Create pipe |
| 17 | sys_ioctl | Device control |
| 18 | sys_getenv | Get environment variable |
| 19 | sys_setenv | Set environment variable |
| 20 | sys_signal | Set signal handler |
| 21 | sys_kill | Send signal |
| 22 | sys_fork | Fork process |
| 23 | sys_execve | Execute program |
| 24 | sys_waitpid | Wait for process |
| 25 | sys_getentropy | Get random bytes |
| 26 | sys_isatty | Test if terminal |

## Project Status

- [x] OS kernel structure
- [x] Bootloader (Multiboot2)
- [x] Memory management (PMM, VMM, heap)
- [x] Interrupt handling (IDT, ISR, IRQ)
- [x] Device drivers (VGA, keyboard, timer)
- [x] System call interface
- [x] CMake build system
- [x] CPython fork configuration
- [x] pyconfig.h for CustomPython OS
- [x] _cpythonos module
- [ ] Full filesystem implementation
- [ ] Complete syscall implementations
- [ ] CPython port (freeze modules, etc.)
- [ ] Autocompiler
- [ ] Package manager
- [ ] Standard library subset

## License

This project inherits the Python Software Foundation License v2 from CPython.
The CustomPython OS kernel code is released under the same license.
