; VGA Text Mode Driver for CustomPython OS
; Directly writes to VGA text buffer at 0xB8000

section .text
global vga_init
global vga_clear
global vga_print_char
global vga_print_string
global vga_set_color
global vga_scroll

VGA_BUFFER   equ 0xB8000
VGA_WIDTH    equ 80
VGA_HEIGHT   equ 25

section .data
vga_row: db 0
vga_col: db 0
vga_color: db 0x0F  ; white on black

section .text

; Initialize VGA driver
vga_init:
    mov byte [vga_row], 0
    mov byte [vga_col], 0
    mov byte [vga_color], 0x0F
    call vga_clear
    ret

; Clear the screen
vga_clear:
    push rax
    push rcx
    push rdi

    mov rdi, VGA_BUFFER
    mov rcx, VGA_WIDTH * VGA_HEIGHT
    mov ax, 0x0F20  ; space with white-on-black color
    rep stosw

    mov byte [vga_row], 0
    mov byte [vga_col], 0

    pop rdi
    pop rcx
    pop rax
    ret

; Print a character to the screen
; AL = character
vga_print_char:
    push rbx
    push rdx

    cmp al, 0x0A  ; newline
    je .newline
    cmp al, 0x0D  ; carriage return
    je .carriage_return
    cmp al, 0x08  ; backspace
    je .backspace

    ; Calculate buffer position
    movzx ebx, byte [vga_row]
    imul ebx, VGA_WIDTH
    movzx edx, byte [vga_col]
    add ebx, edx
    shl ebx, 1  ; * 2 (each cell is 2 bytes)
    add rbx, VGA_BUFFER

    ; Write character + color
    mov ah, [vga_color]
    mov [rbx], ax

    ; Advance column
    inc byte [vga_col]
    cmp byte [vga_col], VGA_WIDTH
    jl .done

    ; Wrap to next line
    mov byte [vga_col], 0
    inc byte [vga_row]
    cmp byte [vga_row], VGA_HEIGHT
    jl .done
    call vga_scroll
    dec byte [vga_row]

    jmp .done

.newline:
    mov byte [vga_col], 0
    inc byte [vga_row]
    cmp byte [vga_row], VGA_HEIGHT
    jl .done
    call vga_scroll
    dec byte [vga_row]
    jmp .done

.carriage_return:
    mov byte [vga_col], 0
    jmp .done

.backspace:
    cmp byte [vga_col], 0
    je .done
    dec byte [vga_col]
    ; Clear the character
    movzx ebx, byte [vga_row]
    imul ebx, VGA_WIDTH
    movzx edx, byte [vga_col]
    add ebx, edx
    shl ebx, 1
    add rbx, VGA_BUFFER
    mov word [rbx], 0x0F20
    jmp .done

.done:
    pop rdx
    pop rbx
    ret

; Print a null-terminated string
; RSI = pointer to string
vga_print_string:
    push rax
    push rsi
.loop:
    lodsb
    test al, al
    jz .done
    call vga_print_char
    jmp .loop
.done:
    pop rsi
    pop rax
    ret

; Set text color
; AL = color attribute (high nibble = bg, low nibble = fg)
vga_set_color:
    mov [vga_color], al
    ret

; Scroll the screen up one line
vga_scroll:
    push rax
    push rcx
    push rdi
    push rsi

    ; Copy lines 1-24 to lines 0-23
    mov rsi, VGA_BUFFER + VGA_WIDTH * 2  ; line 1
    mov rdi, VGA_BUFFER                  ; line 0
    mov rcx, VGA_WIDTH * (VGA_HEIGHT - 1)
    rep movsw

    ; Clear the last line
    mov rcx, VGA_WIDTH
    mov ax, 0x0F20
    rep stosw

    pop rsi
    pop rdi
    pop rcx
    pop rax
    ret

; Get current cursor position
; Returns: RAX = row, RCX = column
vga_get_cursor:
    movzx rax, byte [vga_row]
    movzx rcx, byte [vga_col]
    ret

; Set cursor position
; RDI = row, RSI = column
vga_set_cursor:
    mov [vga_row], dil
    mov [vga_col], sil
    ret
