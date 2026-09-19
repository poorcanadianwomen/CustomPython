; Physical Memory Manager for CustomPython OS
; Bitmap-based physical page allocator

section .text
global pmm_init
global pmm_alloc_page
global pmm_free_page
global pmm_get_total_pages
global pmm_get_free_pages

; Initialize the physical memory manager
; RDI = memory map from bootloader (Multiboot2)
pmm_init:
    push rbx
    push rcx
    push rdx
    push rsi
    push rdi

    ; Assume we have at least 128MB of RAM for now
    ; Set up bitmap at a fixed location (after kernel BSS)
    mov rax, pmm_bitmap
    mov [pmm_bitmap_addr], rax

    ; Calculate number of pages (assume 128MB for now)
    ; 128MB / 4KB = 32768 pages
    mov rax, 128 * 1024 * 1024 / 4096
    mov [pmm_total_pages], rax

    ; Calculate bitmap size (1 bit per page)
    ; 32768 pages / 8 bits = 4096 bytes
    mov rcx, rax
    shr rcx, 3
    mov [pmm_bitmap_size], rcx

    ; Clear bitmap (mark all pages as free)
    mov rdi, rax
    mov rax, 0xFF        ; Mark all as used first
    mov rcx, [pmm_bitmap_size]
    rep stosb

    ; Mark first 1MB + kernel as used (first 256 pages = 1MB)
    mov rdi, [pmm_bitmap_addr]
    mov rcx, 256
.mark_used:
    btr [rdi], rcx
    inc rcx
    cmp rcx, 256
    jl .mark_used

    pop rdi
    pop rsi
    pop rdx
    pop rcx
    pop rbx
    ret

; Allocate a single physical page
; Returns: RAX = physical address of allocated page (0 on failure)
pmm_alloc_page:
    push rbx
    push rcx
    push rdx

    mov rdi, [pmm_bitmap_addr]
    mov rcx, [pmm_total_pages]
    xor rax, rax

.find_free:
    cmp rax, rcx
    jge .not_found

    ; Test bit in bitmap
    bt [rdi], rax
    jnc .found

    inc rax
    jmp .find_free

.found:
    ; Mark page as used
    bts [rdi], rax

    ; Convert page number to physical address
    shl rax, 12          ; * 4096

    pop rdx
    pop rcx
    pop rbx
    ret

.not_found:
    xor eax, eax         ; Return NULL
    pop rdx
    pop rcx
    pop rbx
    ret

; Free a physical page
; RDI = physical address of page to free
pmm_free_page:
    push rbx

    ; Convert address to page number
    shr rdi, 12          ; / 4096

    ; Clear bit in bitmap
    mov rax, [pmm_bitmap_addr]
    btr [rax], rdi

    pop rbx
    ret

; Get total number of pages
pmm_get_total_pages:
    mov rax, [pmm_total_pages]
    ret

; Get number of free pages
pmm_get_free_pages:
    push rbx
    push rcx

    mov rdi, [pmm_bitmap_addr]
    mov rcx, [pmm_total_pages]
    xor rax, rax
    xor rbx, rbx

.count_free:
    cmp rbx, rcx
    jge .done
    bt [rdi], rbx
    jnc .is_free
    inc rbx
    jmp .count_free

.is_free:
    inc rax
    inc rbx
    jmp .count_free

.done:
    pop rcx
    pop rbx
    ret

section .data
pmm_bitmap_addr: dq 0
pmm_total_pages: dq 0
pmm_bitmap_size: dq 0

section .bss
align 4096
pmm_bitmap: resb 16384  ; 128KB bitmap (supports 1M pages = 4GB RAM)
