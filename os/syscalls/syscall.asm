; System Call Interface for CustomPython OS
; Uses x86-64 syscall instruction (MSR 0xC0000082)
; Syscall number in RAX, arguments in RDI, RSI, RDX, R10, R8, R9

section .text
global syscall_handler
global syscall_install
extern syscall_table

; Syscall numbers
SYS_EXIT           equ 0
SYS_READ           equ 1
SYS_WRITE          equ 2
SYS_OPEN           equ 3
SYS_CLOSE          equ 4
SYS_FSTAT          equ 5
SYS_MMAP           equ 6
SYS_MUNMAP         equ 7
SYS_BRK            equ 8
SYS_NANOSLEEP      equ 9
SYS_CLOCK_GETTIME  equ 10
SYS_GETCWD         equ 11
SYS_CHDIR          equ 12
SYS_STAT           equ 13
SYS_DUP            equ 14
SYS_DUP2           equ 15
SYS_PIPE           equ 16
SYS_IOCTL          equ 17
SYS_GETENV         equ 18
SYS_SETENV         equ 19
SYS_SIGNAL         equ 20
SYS_KILL           equ 21
SYS_FORK           equ 22
SYS_EXECVE         equ 23
SYS_WAITPID        equ 24
SYS_GETENTROPY     equ 25
SYS_ISATTY         equ 26
SYS_MAX            equ 27

; Install syscall handler
syscall_install:
    ; Set up SYSCALL MSR registers
    ; IA32_EFER (0xC0000080) - already has LME set

    ; IA32_STAR (0xC0000081) - syscall CS/SS
    mov ecx, 0xC0000081
    xor eax, eax
    mov edx, 0x00180008   ; SYSCALL CS=0x08, SS=0x18; SYSRET CS=0x33, SS=0x3B
    wrmsr

    ; IA32_LSTAR (0xC0000082) - syscall entry point
    mov ecx, 0xC0000082
    lea rax, [rel syscall_entry]
    mov rdx, rax
    shr rdx, 32
    wrmsr

    ; IA32_FMASK (0xC0000084) - interrupt mask during syscall
    mov ecx, 0xC0000084
    xor eax, eax
    xor edx, edx
    wrmsr

    ret

; Syscall entry point (called via SYSCALL instruction)
; On entry: RAX = syscall number, RDI, RSI, RDX, R10, R8, R9 = args
;           RCX = return address, R11 = saved RFLAGS
syscall_entry:
    ; Save registers
    push r11
    push rcx
    push rdx
    push rsi
    push rdi
    push r8
    push r9
    push r10
    push rbp
    push rbx
    push r12
    push r13
    push r14
    push r15

    ; Validate syscall number
    cmp rax, SYS_MAX
    jae .invalid_syscall

    ; Look up handler in syscall table
    lea rbx, [rel syscall_table]
    mov rax, [rbx + rax * 8]

    ; Call handler
    ; RDI, RSI, RDX, R10, R8, R9 are already set up
    mov rdi, rdi      ; Arg 1
    mov rsi, rsi      ; Arg 2
    mov rdx, rdx      ; Arg 3
    mov rcx, r10      ; Arg 4 (R10 -> RCX for C calling convention)
    mov r8, r8        ; Arg 5
    mov r9, r9        ; Arg 6

    call rax

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
    pop rbx

    ; Return via SYSRET
    pop rdi
    pop rsi
    pop rdx
    pop rcx
    pop r11

    sysretq

.invalid_syscall:
    mov rax, -1      ; Return -ENOSYS

    pop r15
    pop r14
    pop r13
    pop r12
    pop r11
    pop r10
    pop r9
    pop r8
    pop rbp
    pop rbx

    pop rdi
    pop rsi
    pop rdx
    pop rcx
    pop r11

    sysretq

section .data
align 8
syscall_table:
    dq sys_exit          ; 0
    dq sys_read          ; 1
    dq sys_write         ; 2
    dq sys_open          ; 3
    dq sys_close         ; 4
    dq sys_fstat         ; 5
    dq sys_mmap          ; 6
    dq sys_munmap        ; 7
    dq sys_brk           ; 8
    dq sys_nanosleep     ; 9
    dq sys_clock_gettime ; 10
    dq sys_getcwd        ; 11
    dq sys_chdir         ; 12
    dq sys_stat          ; 13
    dq sys_dup           ; 14
    dq sys_dup2          ; 15
    dq sys_pipe          ; 16
    dq sys_ioctl         ; 17
    dq sys_getenv        ; 18
    dq sys_setenv        ; 19
    dq sys_signal        ; 20
    dq sys_kill          ; 21
    dq sys_fork          ; 22
    dq sys_execve        ; 23
    dq sys_waitpid       ; 24
    dq sys_getentropy    ; 25
    dq sys_isatty        ; 26

; Syscall implementations (stubs - will be filled in)
section .text

sys_exit:
    ; TODO: Implement exit
    cli
    hlt
    ret

sys_read:
    ; TODO: Implement read
    mov rax, -1
    ret

sys_write:
    ; TODO: Implement write
    mov rax, -1
    ret

sys_open:
    ; TODO: Implement open
    mov rax, -1
    ret

sys_close:
    ; TODO: Implement close
    mov rax, -1
    ret

sys_fstat:
    ; TODO: Implement fstat
    mov rax, -1
    ret

sys_mmap:
    ; TODO: Implement mmap
    mov rax, -1
    ret

sys_munmap:
    ; TODO: Implement munmap
    mov rax, -1
    ret

sys_brk:
    ; TODO: Implement brk
    mov rax, -1
    ret

sys_nanosleep:
    ; TODO: Implement nanosleep
    mov rax, 0
    ret

sys_clock_gettime:
    ; TODO: Implement clock_gettime
    mov rax, -1
    ret

sys_getcwd:
    ; TODO: Implement getcwd
    mov rax, -1
    ret

sys_chdir:
    ; TODO: Implement chdir
    mov rax, -1
    ret

sys_stat:
    ; TODO: Implement stat
    mov rax, -1
    ret

sys_dup:
    ; TODO: Implement dup
    mov rax, -1
    ret

sys_dup2:
    ; TODO: Implement dup2
    mov rax, -1
    ret

sys_pipe:
    ; TODO: Implement pipe
    mov rax, -1
    ret

sys_ioctl:
    ; TODO: Implement ioctl
    mov rax, -1
    ret

sys_getenv:
    ; TODO: Implement getenv
    mov rax, 0
    ret

sys_setenv:
    ; TODO: Implement setenv
    mov rax, 0
    ret

sys_signal:
    ; TODO: Implement signal
    mov rax, 0
    ret

sys_kill:
    ; TODO: Implement kill
    mov rax, -1
    ret

sys_fork:
    ; TODO: Implement fork
    mov rax, -1
    ret

sys_execve:
    ; TODO: Implement execve
    mov rax, -1
    ret

sys_waitpid:
    ; TODO: Implement waitpid
    mov rax, -1
    ret

sys_getentropy:
    ; TODO: Implement getentropy
    mov rax, -1
    ret

sys_isatty:
    ; TODO: Implement isatty
    mov rax, 1  ; Assume stdout is a tty for now
    ret
