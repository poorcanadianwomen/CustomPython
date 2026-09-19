# CustomPython Framework

A custom fork of CPython 3.16.0a0 designed for **Vantrel OS** — featuring a built-in x86-64 ASM operating system kernel, CMake build system, and Python-to-ASM autocompiler.

## Overview

CustomPython brings Python to bare metal by bundling a minimal OS kernel with CPython, allowing Python programs to run directly on hardware without a traditional OS layer.

## Project Structure

```
CustomPython/
├── os/                         # x86-64 ASM OS Kernel
│   ├── boot/                   # Multiboot2 bootloader
│   ├── drivers/                # VGA, keyboard, timer
│   ├── gdt/                    # Global Descriptor Table
│   ├── idt/                    # Interrupt Descriptor Table
│   ├── mm/                     # Memory management (PMM, VMM, heap)
│   ├── fs/                     # Virtual filesystem
│   ├── syscalls/               # System call interface (27 syscalls)
│   └── kernel.c                # Kernel entry point
├── Include/cpythonos/          # Custom pyconfig.h for Vantrel OS
├── Lib/cpythonos/              # Python standard library subset
├── Platform/CustomPython/      # CMake platform config + _cpythonos module
├── Tools/
│   ├── autocompiler/           # Python -> x86-64 ASM transpiler
│   └── pkgmanager/             # Package manager (cpm)
├── cmake/                      # CMake modules
├── CMakeLists.txt              # Top-level CMake build
└── build.sh                    # Quick build script
```

## Requirements

- **Linux** (or WSL2)
- **CMake** >= 3.20
- **NASM** (Netwide Assembler)
- **GCC** (cross-compiler or native)
- **GRUB** (for ISO creation)
- **QEMU** (for testing)

```bash
sudo apt install cmake nasm gcc grub-pc-bin grub-common xorriso mtools qemu-system-x86
```

## Quick Start

```bash
chmod +x build.sh
./build.sh
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

### OS Kernel
- Multiboot2-compliant bootloader
- 64-bit long mode with page tables
- Physical & virtual memory management
- Heap allocator for CPython malloc/free
- PS/2 keyboard, PIT timer, VGA text-mode drivers
- 27 syscalls (exit, read, write, open, mmap, fork, execve, etc.)
- Virtual filesystem abstraction

### CPython Integration
- CPython 3.16.0a0 core (interpreter, parser, objects)
- CMake build system (replaces autoconf/make)
- `_cpythonos` C extension module for OS syscalls
- Static linking, reduced stdlib for bare-metal use

### Autocompiler (WIP)
- Transpiles Python to x86-64 ASM
- Generates ELF binaries for Vantrel OS
- Bootstrappable (written in C)

## Syscall Reference

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
| 9-26 | ... | sleep, time, dir, dup, pipe, ioctl, env, signal, fork, exec, wait, random, isatty |

## Status

- [x] OS kernel (boot, memory, interrupts, drivers, syscalls)
- [x] CMake build system
- [x] CPython fork configuration
- [x] `_cpythonos` module
- [ ] Full filesystem implementation
- [ ] Complete syscall implementations
- [ ] CPython port (freeze modules, etc.)
- [ ] Autocompiler
- [ ] Package manager

## License

Python Software Foundation License v2 (inherited from CPython).
