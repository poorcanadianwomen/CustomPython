/* CustomPython OS Kernel
 * Main entry point and initialization
 */

#include <stdint.h>
#include <stddef.h>

/* Forward declarations of ASM functions */
extern void vga_init(void);
extern void vga_clear(void);
extern void vga_print_string(const char *str);
extern void vga_set_color(uint8_t color);
extern void gdt_install(void);
extern void idt_install(void);
extern void isr_install(void);
extern void irq_install(void);
extern void timer_init(void);
extern void keyboard_init(void);
extern void pmm_init(void *mb_info);
extern void vmm_init(void);
extern void syscall_install(void);
extern void heap_init(void);
extern void vfs_init(void);

/* Forward declarations */
void kernel_main(uint64_t mb_info_addr);

/* VGA color constants */
#define VGA_COLOR_WHITE  0x0F
#define VGA_COLOR_GREEN  0x0A
#define VGA_COLOR_RED    0x04
#define VGA_COLOR_YELLOW 0x0E
#define VGA_COLOR_CYAN   0x0B

/* Print a number in decimal */
void print_number(uint64_t num) {
    char buf[21];
    int i = 20;
    buf[i] = '\0';

    if (num == 0) {
        buf[--i] = '0';
    } else {
        while (num > 0) {
            buf[--i] = '0' + (num % 10);
            num /= 10;
        }
    }

    vga_print_string(&buf[i]);
}

/* Main kernel entry point */
void kernel_main(uint64_t mb_info_addr) {
    /* Initialize VGA for output */
    vga_init();
    vga_clear();

    /* Print boot banner */
    vga_set_color(VGA_COLOR_CYAN);
    vga_print_string("CustomPython OS v0.1.0\n");
    vga_set_color(VGA_COLOR_WHITE);
    vga_print_string("================================\n\n");

    /* Initialize GDT */
    vga_set_color(VGA_COLOR_GREEN);
    vga_print_string("[INIT] ");
    vga_set_color(VGA_COLOR_WHITE);
    vga_print_string("Installing GDT... ");
    gdt_install();
    vga_print_string("OK\n");

    /* Initialize IDT */
    vga_set_color(VGA_COLOR_GREEN);
    vga_print_string("[INIT] ");
    vga_set_color(VGA_COLOR_WHITE);
    vga_print_string("Installing IDT... ");
    idt_install();
    vga_print_string("OK\n");

    /* Initialize PIC and ISR */
    vga_set_color(VGA_COLOR_GREEN);
    vga_print_string("[INIT] ");
    vga_set_color(VGA_COLOR_WHITE);
    vga_print_string("Installing ISR/IRQ... ");
    isr_install();
    vga_print_string("OK\n");

    /* Initialize Physical Memory Manager */
    vga_set_color(VGA_COLOR_GREEN);
    vga_print_string("[INIT] ");
    vga_set_color(VGA_COLOR_WHITE);
    vga_print_string("Initializing PMM... ");
    pmm_init((void *)mb_info_addr);
    vga_print_string("OK\n");

    /* Initialize Virtual Memory Manager */
    vga_set_color(VGA_COLOR_GREEN);
    vga_print_string("[INIT] ");
    vga_set_color(VGA_COLOR_WHITE);
    vga_print_string("Initializing VMM... ");
    vmm_init();
    vga_print_string("OK\n");

    /* Initialize Heap */
    vga_set_color(VGA_COLOR_GREEN);
    vga_print_string("[INIT] ");
    vga_set_color(VGA_COLOR_WHITE);
    vga_print_string("Initializing heap allocator... ");
    heap_init();
    vga_print_string("OK\n");

    /* Initialize VFS */
    vga_set_color(VGA_COLOR_GREEN);
    vga_print_string("[INIT] ");
    vga_set_color(VGA_COLOR_WHITE);
    vga_print_string("Initializing VFS... ");
    vfs_init();
    vga_print_string("OK\n");

    /* Initialize Timer */
    vga_set_color(VGA_COLOR_GREEN);
    vga_print_string("[INIT] ");
    vga_set_color(VGA_COLOR_WHITE);
    vga_print_string("Initializing timer... ");
    timer_init();
    vga_print_string("OK\n");

    /* Initialize Keyboard */
    vga_set_color(VGA_COLOR_GREEN);
    vga_print_string("[INIT] ");
    vga_set_color(VGA_COLOR_WHITE);
    vga_print_string("Initializing keyboard... ");
    keyboard_init();
    vga_print_string("OK\n");

    /* Install Syscall Interface */
    vga_set_color(VGA_COLOR_GREEN);
    vga_print_string("[INIT] ");
    vga_set_color(VGA_COLOR_WHITE);
    vga_print_string("Installing syscall interface... ");
    syscall_install();
    vga_print_string("OK\n");

    /* Enable interrupts */
    vga_set_color(VGA_COLOR_GREEN);
    vga_print_string("[INIT] ");
    vga_set_color(VGA_COLOR_WHITE);
    vga_print_string("Enabling interrupts... ");
    irq_install();
    vga_print_string("OK\n");

    /* Print completion message */
    vga_print_string("\n");
    vga_set_color(VGA_COLOR_GREEN);
    vga_print_string("[READY] ");
    vga_set_color(VGA_COLOR_WHITE);
    vga_print_string("CustomPython OS initialized successfully!\n\n");

    vga_set_color(VGA_COLOR_YELLOW);
    vga_print_string("System ready. Loading CustomPython interpreter...\n");
    vga_set_color(VGA_COLOR_WHITE);

    /* TODO: Load and start CustomPython interpreter */
    /* For now, just halt */
    while (1) {
        __asm__ volatile("hlt");
    }
}
