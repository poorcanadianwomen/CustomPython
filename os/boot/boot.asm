; CustomPython OS Bootloader
; Multiboot2 compliant, transitions from 32-bit protected mode to 64-bit long mode

MB2_MAGIC      equ 0xE85250D6
MB2_ARCH       equ 0              ; i386 (protected mode)
MB2_HEADER_LEN equ header_end - header_start
MB2_CHECKSUM   equ -(MB2_MAGIC + MB2_ARCH + MB2_HEADER_LEN)

section .multiboot2
header_start:
    dd MB2_MAGIC
    dd MB2_ARCH
    dd MB2_HEADER_LEN
    dd MB2_CHECKSUM

    ; End tag
    dw 0
    dw 0
    dd 8
header_end:

section .bss
align 16
stack_bottom:
    resb 16384
stack_top:

section .text
global _start
extern kernel_main

bits 32
_start:
    cli

    mov esp, stack_top

    ; Save boot info pointer
    push ebx
    push eax

    ; Check for Multiboot2
    cmp eax, MB2_MAGIC
    jne .no_multiboot

    ; Save multiboot info physical address
    mov [mb_info_addr], ebx

    ; Check for CPUID support (flip ID bit in EFLAGS)
    pushfd
    pop eax
    mov ecx, eax
    xor eax, 1 << 21
    push eax
    popfd
    pushfd
    pop eax
    push ecx
    popfd
    xor eax, ecx
    jz .no_long_mode

    ; Check for extended CPUID
    mov eax, 0x80000001
    cpuid
    test edx, 1 << 29
    jz .no_long_mode

    ; Check for SSE
    mov eax, 1
    cpuid
    test edx, 1 << 25
    jz .no_sse

    ; Enable SSE and AVX (if available)
    mov eax, cr4
    or eax, 1 << 9      ; OSFXSR
    or eax, 1 << 10     ; OSXMMEXCPT
    mov cr4, eax

    ; Set up page tables for identity mapping + higher half
    call setup_page_tables
    test eax, eax
    jnz .page_tables_failed

    ; Enable PAE
    mov eax, cr4
    or eax, 1 << 5
    mov cr4, eax

    ; Load PML4 into CR3
    mov eax, pml4_table
    mov cr3, eax

    ; Enable long mode (EFER.LME)
    mov ecx, 0xC0000080
    rdmsr
    or eax, 1 << 8
    wrmsr

    ; Enable paging (CR0.PG) and protected mode (CR0.PE)
    mov eax, cr0
    or eax, (1 << 31) | (1 << 0)
    mov cr0, eax

    ; Load 64-bit GDT
    lgdt [gdt64_descriptor]

    ; Jump to 64-bit code
    jmp 0x08:long_mode_start

.no_multiboot:
    mov esi, msg_no_multiboot
    call print_string_32
    jmp halt

.no_long_mode:
    mov esi, msg_no_long_mode
    call print_string_32
    jmp halt

.no_sse:
    mov esi, msg_no_sse
    call print_string_32
    jmp halt

.page_tables_failed:
    mov esi, msg_page_fail
    call print_string_32
    jmp halt

; Print string in 32-bit protected mode (VGA text buffer)
print_string_32:
    mov edi, 0xB8000
    mov ah, 0x0F
.loop:
    lodsb
    test al, al
    jz .done
    stosw
    jmp .loop
.done:
    ret

halt:
    hlt
    jmp halt

; Set up identity mapping + higher-half mapping for first 2MB using 2MB pages
setup_page_tables:
    ; Clear page tables
    mov edi, pml4_table
    mov ecx, 4096 * 5 / 4
    xor eax, eax
    rep stosd

    ; PML4[0] -> PDPT
    mov eax, pdpt_table
    or eax, 0x03  ; present + writable
    mov [pml4_table], eax

    ; PML4[512] -> PDPT (higher half at 0xFFFF800000000000)
    mov [pml4_table + 512 * 8], eax

    ; PDPT[0] -> PD (for identity mapping)
    mov eax, pd_table
    or eax, 0x03
    mov [pdpt_table], eax

    ; PDPT[512] -> PD (for higher half)
    mov [pdpt_table + 512 * 8], eax

    ; Identity map first 2GB using 2MB pages
    mov eax, 0x00000083  ; present + writable + PS (page size = 2MB)
    mov edi, pd_table
    mov ecx, 0  ; counter for pages mapped

.map_loop:
    cmp ecx, 1024  ; 1024 * 2MB = 2GB
    jge .map_done

    mov [edi], eax
    add eax, 0x200000  ; next 2MB page
    add edi, 8
    inc ecx
    jmp .map_loop

.map_done:
    xor eax, eax
    ret

; Data
section .data
align 4096

msg_no_multiboot: db "ERROR: Not booted with Multiboot2 compliant bootloader", 0
msg_no_long_mode:  db "ERROR: 64-bit long mode not supported", 0
msg_no_sse:        db "ERROR: SSE not supported", 0
msg_page_fail:     db "ERROR: Failed to set up page tables", 0

mb_info_addr: dq 0

; GDT for 64-bit mode
align 16
gdt64:
    ; Null descriptor
    dq 0
    ; Code segment (0x08)
    dw 0          ; Limit (ignored in long mode)
    dw 0          ; Base (ignored in long mode)
    db 0          ; Base
    db 10011010b  ; Access: present, ring 0, code, readable
    db 10100000b  ; Flags: long mode
    db 0          ; Base
    ; Data segment (0x10)
    dw 0
    dw 0
    db 0
    db 10010010b  ; Access: present, ring 0, data, writable
    db 11000000b  ; Flags: 64-bit
    db 0
gdt64_end:

gdt64_descriptor:
    dw gdt64_end - gdt64 - 1
    dq gdt64

; Page tables (aligned to 4096 bytes)
section .bss
align 4096
pml4_table: resb 4096
pdpt_table: resb 4096
pd_table:   resb 4096
pt_table:   resb 4096

; 64-bit long mode entry
section .text
bits 64
long_mode_start:
    ; Set up data segments
    mov ax, 0x10
    mov ds, ax
    mov es, ax
    mov fs, ax
    mov gs, ax
    mov ss, ax

    ; Set up stack (use higher-half address)
    mov rsp, stack_top + 0xFFFF800000000000

    ; Restore multiboot info pointer
    mov rdi, [mb_info_addr]

    ; Call kernel main
    call kernel_main

    ; If kernel returns, halt
    cli
.halt:
    hlt
    jmp .halt
