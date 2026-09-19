#!/bin/bash
# Create bootable ISO for CustomPython OS
# Requires: grub-pc-bin, grub-common, xorriso, mtools

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "${SCRIPT_DIR}")"
BUILD_DIR="${PROJECT_DIR}/build"
ISO_DIR="${BUILD_DIR}/iso"
ISO_FILE="${BUILD_DIR}/custompython.iso"

echo "Creating bootable ISO..."

# Clean previous ISO
rm -f "${ISO_FILE}"
rm -rf "${ISO_DIR}"

# Create ISO directory structure
mkdir -p "${ISO_DIR}/boot/grub"

# Copy kernel
cp "${BUILD_DIR}/os/custompython-kernel" "${ISO_DIR}/boot/"

# Copy GRUB configuration
cat > "${ISO_DIR}/boot/grub/grub.cfg" << 'EOF'
set timeout=5
set default=0

menuentry "CustomPython OS" {
    multiboot2 /boot/custompython-kernel
    boot
}

menuentry "CustomPython OS (Serial Console)" {
    multiboot2 /boot/custompython-kernel console=serial
    boot
}
EOF

# Create GRUB modules list
cat > "${ISO_DIR}/boot/grub/grub.cfg" << 'EOF'
set timeout=5
set default=0

menuentry "CustomPython OS" {
    multiboot2 /boot/custompython-kernel
    boot
}
EOF

# Create the ISO
grub-mkrescue \
    --output="${ISO_FILE}" \
    --modules="part_msdos iso9660 biosdisk" \
    "${ISO_DIR}"

echo ""
echo "ISO created: ${ISO_FILE}"
echo ""
echo "To run in QEMU:"
echo "  qemu-system-x86_64 -cdrom ${ISO_FILE} -m 256M -serial stdio"
echo ""
echo "To write to USB (DANGEROUS - double check device!):"
echo "  sudo dd if=${ISO_FILE} of=/dev/sdX bs=4M status=progress"
echo ""
