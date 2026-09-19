; PIT (Programmable Interval Timer) Driver for CustomPython OS
; Provides system tick counter for time module

PIT_FREQUENCY equ 1193182   ; Base PIT frequency in Hz
PIT_DIVIDER    equ 100      ; 100 Hz = 10ms per tick

section .text
global timer_init
global timer_handler
global timer_get_ticks
global timer_get_seconds

timer_init:
    ; Configure PIT channel 0 for rate generator
    mov al, 00110110b   ; Channel 0, lobyte/hibyte, rate generator
    out 0x43, al

    ; Set divisor for ~100 Hz
    mov eax, PIT_FREQUENCY / PIT_DIVIDER
    out 0x40, al        ; Low byte
    mov al, ah
    out 0x40, al        ; High byte

    ; Enable IRQ0 (timer)
    in al, 0x21
    and al, 0xFE        ; Clear bit 0 (enable IRQ0)
    out 0x21, al

    ret

; Timer handler called from IRQ0
timer_handler:
    push rax

    ; Increment tick counter
    inc qword [timer_ticks]

    ; Send EOI to PIC
    mov al, 0x20
    out 0x20, al

    pop rax
    ret

; Get current tick count
; Returns: RAX = number of ticks since boot
timer_get_ticks:
    mov rax, [timer_ticks]
    ret

; Get seconds since boot (approximate)
; Returns: RAX = seconds
timer_get_seconds:
    mov rax, [timer_ticks]
    xor rdx, rdx
    mov rcx, PIT_DIVIDER
    div rcx
    ret

; Sleep for specified number of ticks
; RDI = number of ticks to sleep
global timer_sleep
timer_sleep:
    push rbx
    mov rbx, rdi
    add rbx, [timer_ticks]

.wait:
    pause
    cmp [timer_ticks], rbx
    jl .wait

    pop rbx
    ret

section .data
timer_ticks: dq 0
