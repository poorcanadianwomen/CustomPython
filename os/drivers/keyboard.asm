; PS/2 Keyboard Driver for CustomPython OS
; Handles IRQ1 (interrupt 33)

section .text
global keyboard_init
global keyboard_handler

keyboard_init:
    ; Enable keyboard IRQ (IRQ1)
    in al, 0x21
    and al, 0xFD     ; Clear bit 1 (enable IRQ1)
    out 0x21, al
    ret

; Keyboard handler called from IRQ1
keyboard_handler:
    push rax
    push rbx

    ; Read scancode from port 0x60
    in al, 0x60

    ; Store scancode in buffer
    movzx ebx, byte [kb_buffer_end]
    mov [kb_buffer + ebx], al
    inc bl
    and bl, 0x3F     ; Wrap buffer (64 entries)
    mov [kb_buffer_end], bl

    ; Send EOI to PIC
    mov al, 0x20
    out 0x20, al

    pop rbx
    pop rax
    ret

; Get a key from the buffer (non-blocking)
; Returns: AL = scancode (0 if buffer empty)
global keyboard_get_key
keyboard_get_key:
    push rbx

    movzx eax, byte [kb_buffer_start]
    movzx ebx, byte [kb_buffer_end]
    cmp eax, ebx
    je .empty

    mov al, [kb_buffer + eax]
    inc byte [kb_buffer_start]
    and byte [kb_buffer_start], 0x3F

    pop rbx
    ret

.empty:
    xor al, al
    pop rbx
    ret

; Scancode to ASCII lookup table (US QWERTY, make codes only)
section .data
scancode_to_ascii:
    db 0,  27, '1','2','3','4','5','6','7','8','9','0','-','=', 8, 9
    db 'q','w','e','r','t','y','u','i','o','p','[',']', 13, 0
    db 'a','s','d','f','g','h','j','k','l',';',"'",'`', 0, '\'
    db 'z','x','c','v','b','n','m',',','.','/', 0, '*', 0, ' '
    db 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

section .bss
align 64
kb_buffer: resb 64
kb_buffer_start: resb 1
kb_buffer_end: resb 1
