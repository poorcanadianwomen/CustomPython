#!/bin/bash
# Run CustomPython OS in QEMU
# Requires: qemu-system-x86

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "${SCRIPT_DIR}")"
BUILD_DIR="${PROJECT_DIR}/build"
ISO_FILE="${BUILD_DIR}/custompython.iso"

# Check if ISO exists
if [ ! -f "${ISO_FILE}" ]; then
    echo "ISO not found. Building first..."
    "${SCRIPT_DIR}/create_iso.sh"
fi

echo "Starting QEMU..."
echo "  Press Ctrl+A then X to exit"
echo ""

# Run QEMU with common options
qemu-system-x86_64 \
    -cdrom "${ISO_FILE}" \
    -m 256M \
    -serial stdio \
    -display none \
    -no-reboot \
    -no-shutdown \
    -machine q35,accel=kvm 2>/dev/null || \
qemu-system-x86_64 \
    -cdrom "${ISO_FILE}" \
    -m 256M \
    -serial stdio \
    -display none \
    -no-reboot \
    -no-shutdown
