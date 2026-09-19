#!/bin/bash
# CustomPython Build Script
# Builds the OS kernel and CPython interpreter

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUILD_DIR="${SCRIPT_DIR}/build"
BUILD_TYPE="${1:-Release}"

echo "========================================="
echo "  CustomPython Build System"
echo "========================================="
echo ""

# Check for required tools
check_tool() {
    if ! command -v "$1" &> /dev/null; then
        echo "Error: $1 is required but not installed."
        echo "  $2"
        exit 1
    fi
}

echo "Checking build dependencies..."
check_tool "cmake" "Install with: sudo apt install cmake"
check_tool "nasm" "Install with: sudo apt install nasm"
check_tool "gcc" "Install with: sudo apt install gcc"
check_tool "ld" "Install with: sudo apt install binutils"
echo "All dependencies found."
echo ""

# Create build directory
echo "Creating build directory..."
mkdir -p "${BUILD_DIR}"
cd "${BUILD_DIR}"

# Configure with CMake
echo "Configuring with CMake..."
cmake "${SCRIPT_DIR}" \
    -DCMAKE_BUILD_TYPE="${BUILD_TYPE}" \
    -DCUSTOMPYTHON_BUILD_KERNEL=ON \
    -DCUSTOMPYTHON_BUILD_INTERPRETER=ON \
    -DCUSTOMPYTHON_BUILD_AUTOCOMPILER=ON \
    -DCUSTOMPYTHON_STATIC_BUILD=ON

echo ""

# Build
echo "Building..."
cmake --build . -j$(nproc)

echo ""
echo "========================================="
echo "  Build Complete!"
echo "========================================="
echo ""
echo "Kernel: ${BUILD_DIR}/os/custompython-kernel"
echo "Interpreter: ${BUILD_DIR}/Platform/CustomPython/cpython_custompython"
echo "Autocompiler: ${BUILD_DIR}/Tools/autocompiler/autocompiler"
echo ""
echo "To create a bootable ISO:"
echo "  sudo apt install grub-pc-bin grub-common xorriso mtools"
echo "  ./tools/create_iso.sh"
echo ""
echo "To run in QEMU:"
echo "  sudo apt install qemu-system-x86"
echo "  ./tools/run_qemu.sh"
echo ""
