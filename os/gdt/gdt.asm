; Global Descriptor Table for CustomPython OS
; Provides segment descriptors for 64-bit long mode

section .text
global gdt_install
global gdt_flush

; GDT structure
struc gdt_entry
    .limit_low:    resw 1
    .base_low:     resw 1
    .base_middle:  resb 1
    .access:       resb 1
    .granularity:  resb 1
    .base_high:    resb 1
endstruc

struc gdt_ptr
    .limit:  resw 1
    .base:   resd 1
endstruc

section .data
align 16

; GDT entries (null, code, data, user code, user data, TSS)
gdt_entries:
    ; Null descriptor
    dq 0

    ; Kernel code segment (0x08)
    dw 0x0000       ; Limit low
    dw 0x0000       ; Base low
    db 0x00         ; Base middle
    db 10011010b    ; Access: present, ring 0, code, readable, conforming
    db 10100000b    ; Granularity: 64-bit, limit ignored
    db 0x00         ; Base high

    ; Kernel data segment (0x10)
    dw 0x0000
    dw 0x0000
    db 0x00
    db 10010010b    ; Access: present, ring 0, data, writable
    db 11000000b    ; Granularity: 64-bit
    db 0x00

    ; User code segment (0x18)
    dw 0x0000
    dw 0x0000
    db 0x00
    db 11111010b    ; Access: present, ring 3, code, readable
    db 10100000b    ; Granularity: 64-bit
    db 0x00

    ; User data segment (0x20)
    dw 0x0000
    dw 0x0000
    db 0x00
    db 11110010b    ; Access: present, ring 3, data, writable
    db 11000000b    ; Granularity: 64-bit
    db 0x00

    ; TSS descriptor (0x28) - filled in by tss_install
    dq 0

gdt_end:

gdt_ptr_struct:
    dw gdt_end - gdt_entries - 1
    dq gdt_entries

section .text

; Install the GDT
gdt_install:
    lgdt [gdt_ptr_struct]

    ; Reload segment registers
    mov ax, 0x10        ; kernel data segment
    mov ds, ax
    mov es, ax
    mov fs, ax
    mov gs, ax
    mov ss, ax

    ; Reload CS via far return
    push 0x08           ; kernel code segment
    lea rax, [rel .reload_cs]
    push rax
    retfq
.reload_cs:
    ret

; Flush GDT (reload all segment registers)
gdt_flush:
    mov ax, 0x10
    mov ds, ax
    mov es, ax
    mov fs, ax
    mov gs, ax
    mov ss, ax
    ret
