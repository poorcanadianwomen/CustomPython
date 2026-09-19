; Kernel entry point - called from bootloader
; Sets up initial state before calling C kernel_main

section .text
global kernel_entry
extern kernel_main

kernel_entry:
    ; Stack is already set up by bootloader
    ; RDI = multiboot info address (from bootloader)

    ; Clear BSS
    extern __bss_start
    extern __bss_end
    mov rdi, __bss_start
    mov rcx, __bss_end
    sub rcx, rdi
    xor al, al
    rep stosb

    ; Restore multiboot info pointer
    mov rdi, [mb_info_addr]

    ; Call C kernel
    call kernel_main

    ; Halt if kernel returns
    cli
.halt:
    hlt
    jmp .halt

section .data
mb_info_addr: dq 0
