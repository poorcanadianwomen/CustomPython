/* CustomPython OS Linker Script
 * Links the kernel at the correct address
 */

/* Entry point */
ENTRY(_start)

/* Kernel is loaded at 1MB, linked to virtual address 0xFFFFFFFF80000000 */
KERNEL_OFFSET = 0xFFFFFFFF80000000;
KERNEL_PHYS   = 0x00100000;

SECTIONS
{
    /* Code section */
    .text KERNEL_PHYS + KERNEL_OFFSET : AT(KERNEL_PHYS)
    {
        *(.multiboot2)
        *(.text)
    }

    /* Read-only data */
    .rodata ALIGN(4K) : AT(ADDR(.rodata) - KERNEL_OFFSET)
    {
        *(.rodata)
    }

    /* Initialized data */
    .data ALIGN(4K) : AT(ADDR(.data) - KERNEL_OFFSET)
    {
        *(.data)
    }

    /* Uninitialized data (BSS) */
    .bss ALIGN(4K) : AT(ADDR(.bss) - KERNEL_OFFSET)
    {
        __bss_start = .;
        *(.bss)
        *(COMMON)
        __bss_end = .;
    }

    /* Page tables (must be page-aligned) */
    .page_tables ALIGN(4K) : AT(ADDR(.page_tables) - KERNEL_OFFSET)
    {
        *(.page_tables)
    }

    /* Kernel end symbol */
    _kernel_end = .;

    /* Discard unwanted sections */
    /DISCARD/ :
    {
        *(.comment)
        *(.note.*)
        *(.eh_frame*)
    }
}
