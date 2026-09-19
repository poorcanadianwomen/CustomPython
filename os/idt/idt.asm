; Interrupt Descriptor Table for CustomPython OS
; Handles hardware interrupts and exceptions

section .text
global idt_install
global idt_set_gate
global isr_install
global irq_install
global isr_handler
global irq_handler

; ISR (Interrupt Service Routine) stubs
; Each ISR pushes its interrupt number and jumps to common handler

%macro ISR_NOERRCODE 1
global isr%1
isr%1:
    push qword 0        ; Dummy error code
    push qword %1       ; Interrupt number
    jmp isr_common_stub
%endmacro

%macro ISR_ERRCODE 1
global isr%1
isr%1:
    push qword %1       ; Interrupt number
    jmp isr_common_stub
%endmacro

; CPU Exceptions (0-31)
ISR_NOERRCODE 0
ISR_NOERRCODE 1
ISR_NOERRCODE 2
ISR_NOERRCODE 3
ISR_NOERRCODE 4
ISR_NOERRCODE 5
ISR_NOERRCODE 6
ISR_NOERRCODE 7
ISR_ERRCODE   8
ISR_NOERRCODE 9
ISR_ERRCODE   10
ISR_ERRCODE   11
ISR_ERRCODE   12
ISR_ERRCODE   13
ISR_ERRCODE   14
ISR_NOERRCODE 15
ISR_NOERRCODE 16
ISR_ERRCODE   17
ISR_NOERRCODE 18
ISR_NOERRCODE 19
ISR_NOERRCODE 20
ISR_ERRCODE   21
ISR_NOERRCODE 22
ISR_NOERRCODE 23
ISR_NOERRCODE 24
ISR_NOERRCODE 25
ISR_NOERRCODE 26
ISR_NOERRCODE 27
ISR_ERRCODE   28
ISR_NOERRCODE 29
ISR_ERRCODE   30
ISR_NOERRCODE 31

; IRQ (Hardware Interrupt Request) stubs (32-47)
%macro IRQ 2
global irq%1
irq%1:
    push qword 0        ; Dummy error code
    push qword %2       ; Interrupt number (32 + IRQ number)
    jmp irq_common_stub
%endmacro

IRQ  0, 32    ; PIT timer
IRQ  1, 33    ; Keyboard
IRQ  2, 34    ; Cascade
IRQ  3, 35    ; COM2
IRQ  4, 36    ; COM1
IRQ  5, 37    ; LPT2
IRQ  6, 38    ; Floppy
IRQ  7, 39    ; LPT1 / Spurious
IRQ  8, 40    ; CMOS RTC
IRQ  9, 41    ; ACPI
IRQ 10, 42    ; Open
IRQ 11, 43    ; Open
IRQ 12, 44    ; PS/2 Mouse
IRQ 13, 45    ; FPU
IRQ 14, 46    ; Primary ATA
IRQ 15, 47    ; Secondary ATA

; Common ISR handler
isr_common_stub:
    ; Save all general-purpose registers
    push rax
    push rbx
    push rcx
    push rdx
    push rsi
    push rdi
    push rbp
    push r8
    push r9
    push r10
    push r11
    push r12
    push r13
    push r14
    push r15

    ; Call C handler with pointer to registers as argument
    mov rdi, rsp        ; First argument: pointer to interrupt frame
    call isr_handler

    ; Restore registers
    pop r15
    pop r14
    pop r13
    pop r12
    pop r11
    pop r10
    pop r9
    pop r8
    pop rbp
    pop rdi
    pop rsi
    pop rdx
    pop rcx
    pop rbx
    pop rax

    ; Remove error code and interrupt number from stack
    add rsp, 16

    iretq

; Common IRQ handler
irq_common_stub:
    push rax
    push rbx
    push rcx
    push rdx
    push rsi
    push rdi
    push rbp
    push r8
    push r9
    push r10
    push r11
    push r12
    push r13
    push r14
    push r15

    mov rdi, rsp
    call irq_handler

    pop r15
    pop r14
    pop r13
    pop r12
    pop r11
    pop r10
    pop r9
    pop r8
    pop rbp
    pop rdi
    pop rsi
    pop rdx
    pop rcx
    pop rbx
    pop rax

    add rsp, 16

    iretq

section .data
align 16

; IDT structure
idt_entries:
    times 256 dq 0, 0   ; 256 entries, each 16 bytes

idt_ptr:
    dw idt_entries_end - idt_entries - 1
    dq idt_entries

; PIC (8259) remap command bytes
PIC1_COMMAND equ 0x20
PIC1_DATA    equ 0x21
PIC2_COMMAND equ 0xA0
PIC2_DATA    equ 0xA1

section .text

; Install the IDT
idt_install:
    lidt [idt_ptr]
    ret

; Set an IDT gate
; RDI = interrupt number
; RSI = handler address
; DX  = code segment selector
; AL  = flags
idt_set_gate:
    push rbx

    ; Calculate entry address
    mov rbx, rdi
    shl rbx, 4          ; * 16 (each entry is 16 bytes)
    add rbx, idt_entries

    ; Set handler address
    mov [rbx], si                    ; offset low
    mov [rbx + 2], dx               ; segment selector
    mov byte [rbx + 4], al          ; IST and reserved
    mov byte [rbx + 5], 0x8E        ; present, ring 0, interrupt gate

    shr rsi, 16
    mov [rbx + 6], si               ; offset middle

    shr rsi, 16
    mov [rbx + 8], esi              ; offset high

    pop rbx
    ret

; Remap the PIC to avoid conflicts with CPU exceptions
isr_install:
    ; Initialize ICW1
    mov al, 0x11
    out PIC1_COMMAND, al
    out PIC2_COMMAND, al

    ; Initialize ICW2 (offset)
    mov al, 0x20    ; IRQ 0-7 -> INT 32-39
    out PIC1_DATA, al
    mov al, 0x28    ; IRQ 8-15 -> INT 40-47
    out PIC2_DATA, al

    ; Initialize ICW3
    mov al, 0x04    ; PIC1 slave on IRQ2
    out PIC1_DATA, al
    mov al, 0x02    ; PIC2 cascade identity
    out PIC2_DATA, al

    ; Initialize ICW4
    mov al, 0x01    ; 8086 mode
    out PIC1_DATA, al
    out PIC2_DATA, al

    ret

; Enable IRQs
irq_install:
    sti
    ret

; Disable IRQs
global irq_disable
irq_disable:
    cli
    ret
