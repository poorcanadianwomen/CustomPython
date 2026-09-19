/* pyconfig.h for CustomPython OS
 * Generated configuration for CPython running on CustomPython OS
 */

#ifndef Py_PYCONFIG_H
#define Py_PYCONFIG_H

/* CustomPython OS specific */
#define CUSTOMPYTHON_OS 1
#define CUSTOMPYTHON_OS_NAME "CustomPython"
#define CUSTOMPYTHON_ARCH "x86_64"

/* Platform identification */
#define SYS_ARCH "x86_64"
#define SOABI "cpython-316-custompython"
#define MULTIARCH_CPPFLAGS ""

/* Size definitions */
#define SIZEOF_LONG 8
#define SIZEOF_LONG_LONG 8
#define SIZEOF_INT 4
#define SIZEOF_SHORT 2
#define SIZEOF_FLOAT 8
#define SIZEOF_DOUBLE 8
#define SIZEOF_LONG_DOUBLE 16
#define SIZEOF_VOID_P 8
#define SIZEOF_SIZE_T 8
#define SIZEOF_PID_T 4
#define SIZEOF_OFF_T 8
#define SIZEOF_TIME_T 8
#define SIZEOF_UID_T 4
#define SIZEOF_GID_T 4
#define SIZEOF_SIG_ATOMIC_T 4
#define SIZEOF_WCHAR_T 4
#define SIZEOF__BOOL 1

/* Integer types */
#define HAVE_LONG_LONG 1
#define PY_FORMAT_LONG_LONG "ll"
#define PY_FORMAT_SIZE_T "z"

/* Thread support */
#define _POSIX_THREADS 1
#define WITH_THREAD 1
#define THREAD_STACK_SIZE (2 * 1024 * 1024)

/* Memory allocator */
#define WITH_PYMALLOC 1
#define WITH_MIMALLOC 1

/* Enable features */
#define ENABLE_unicode 1
#define Py_USING_MEMORY_DEBUGGER 0
#define Py_BUILD_CORE 1
#define Py_BUILD_CORE_BUILTIN 1

/* Disable unsupported features */
#define HAVE_DLOPEN 0
#define HAVE_DYNAMIC_LOADING 0
#define HAVE_FORK 0
#define HAVE_VFORK 0
#define HAVE_EXECV 0
#define HAVE_PIPE 0
#define HAVE_PIPE2 0
#define HAVE_SOCKET 0
#define HAVE_NETINET_IN_H 0
#define HAVE_ARPA_INET_H 0
#define HAVE_SYS_TYPES_H 0
#define HAVE_SYS_STAT_H 0
#define HAVE_SYS_TIME_H 0
#define HAVE_SYS_TIMES_H 0
#define HAVE_SYS_WAIT_H 0
#define HAVE_SYS_RESOURCE_H 0
#define HAVE_SYS_SOCKET_H 0
#define HAVE_SYS_UN_H 0
#define HAVE_UNISTD_H 0
#define HAVE_FCNTL_H 0
#define HAVE_SIGNAL_H 0
#define HAVE_SYS_SELECT_H 0
#define HAVE_SYS_EPOLL_H 0
#define HAVE_SYS_EVENTFD_H 0
#define HAVE_POLL_H 0
#define HAVE_DLFCN_H 0
#define HAVE_SCHED_H 0
#define HAVE_SEMAPHORE_H 0
#define HAVE_LANGINFO_H 0
#define HAVE_WCHAR_H 0
#define HAVE_STDLIB_H 0
#define HAVE_STRING_H 0
#define HAVE_ERRNO_H 0
#define HAVE_ASSERT_H 0

/* Function availability */
#define HAVE_GETTIMEOFDAY 0
#define HAVE_CLOCK_GETTIME 1
#define HAVE_SIGACTION 0
#define HAVE_KILL 0
#define HAVE_GETPID 0
#define HAVE_GETUID 0
#define HAVE_GETEUID 0
#define HAVE_GETGID 0
#define HAVE_GETEGID 0
#define HAVE_SETUID 0
#define HAVE_SETGID 0
#define HAVE_SETGROUPS 0
#define HAVE_GETPGRP 0
#define HAVE_SETPGID 0
#define HAVE_GETLOGIN 0
#define HAVE_GETPWNAM 0
#define HAVE_GETPWUID 0
#define HAVE_GETGRNAM 0
#define HAVE_GETGRGID 0
#define HAVE_SYS_CONF 0
#define HAVE_LONG_DOUBLE 1
#define HAVE_LONG_LONG 1
#define HAVE_UINT64_T 1
#define HAVE_UINT32_T 1
#define HAVE_UINT16_T 1
#define HAVE_UINT8_T 1
#define HAVE_INT64_T 1
#define HAVE_INT32_T 1
#define HAVE_INT16_T 1
#define HAVE_INT8_T 1
#define HAVE_SSIZE_T 1
#define HAVE__BOOL 1
#define HAVE_FLOAT_H 1
#define HAVE_STDINT_H 1
#define HAVE_CRT_SECURE_COMPILER_WARNING 0
#define HAVE_GCC_UINT128_T 1
#define HAVE_GCC_BUILTIN_FPCLASSIFY 1
#define HAVE_GCC_BUILTIN_ISNAN 1
#define HAVE_GCC_BUILTIN_ISINF 1

/* Random number generation */
#define HAVE_GETRANDOM 1
#define HAVE_GETENTROPY 0

/* Time functions */
#define HAVE_CLOCK_GETTIME 1
#define HAVE_CLOCK_GETTIME_MONOTONIC 1
#define HAVE_CLOCK_GETTIME_REALTIME 1
#define HAVE_CLOCK_GETTIME_PROCESS_CPUTIME_ID 0
#define HAVE_CLOCK_GETTIME_THREAD_CPUTIME_ID 0
#define HAVE_MACH_CLOCK 0

/* File system */
#define HAVE_STAT 0
#define HAVE_FSTAT 0
#define HAVE_LSTAT 0
#define HAVE_ACCESS 0
#define HAVE_GETCWD 0
#define HAVE_CHDIR 0
#define HAVE_READDIR 0
#define HAVE_OPENDIR 0
#define HAVE_CLOSEDIR 0
#define HAVE_MKDIR 0
#define HAVE_RMDIR 0
#define HAVE_UNLINK 0
#define HAVE_RENAME 0
#define HAVE_CHMOD 0
#define HAVE_CHOWN 0
#define HAVE_LINK 0
#define HAVE_SYMLINK 0
#define HAVE_READLINK 0
#define HAVE_REALPATH 0
#define HAVE_TEMPNAM 0
#define HAVE_TMPFILE 0
#define HAVE_TMPNAM 0
#define HAVE_POPEN 0
#define HAVE_SYSTEM 0

/* Memory mapping */
#define HAVE_MMAP 0
#define HAVE_MPROTECT 0
#define HAVE_MUNMAP 0
#define HAVE_MREMAP 0

/* Process management */
#define HAVE_WAIT 0
#define HAVE_WAITPID 0
#define HAVE_GETRUSAGE 0
#define HAVE_GETRLIMIT 0
#define HAVE_SETRLIMIT 0

/* Dynamic loading */
#define HAVE_DLOPEN 0
#define HAVE_DLSYM 0
#define HAVE_DLCLOSE 0
#define HAVE_DLERROR 0

/* Signal handling */
#define HAVE_SIGACTION 0
#define HAVE_SIGRELSE 0
#define HAVE_SIGHOLD 0
#define HAVE_SIGALTSTACK 0
#define HAVE_SIGTIMEDWAIT 0
#define HAVE_SIGWAIT 0
#define HAVE_SIGPENDING 0
#define HAVE_SIGPROCMASK 0
#define HAVE_PTHREAD_SIGMASK 0

/* Threading */
#define _USE_PTHREADS 1
#define WITH_THREAD 1
#define HAVE_PTHREAD_CREATE 0
#define HAVE_PTHREAD_JOIN 0
#define HAVE_PTHREAD_DETACH 0
#define HAVE_PTHREAD_ATTR_INIT 0
#define HAVE_PTHREAD_ATTR_DESTROY 0
#define HAVE_PTHREAD_ATTR_GETSTACKSIZE 0
#define HAVE_PTHREAD_ATTR_SETSTACKSIZE 0
#define HAVE_PTHREAD_CREATE 0
#define HAVE_PTHREAD_MUTEX_INIT 0
#define HAVE_PTHREAD_MUTEX_DESTROY 0
#define HAVE_PTHREAD_MUTEX_LOCK 0
#define HAVE_PTHREAD_MUTEX_UNLOCK 0
#define HAVE_PTHREAD_MUTEX_TRYLOCK 0
#define HAVE_PTHREAD_COND_INIT 0
#define HAVE_PTHREAD_COND_DESTROY 0
#define HAVE_PTHREAD_COND_SIGNAL 0
#define HAVE_PTHREAD_COND_WAIT 0
#define HAVE_PTHREAD_COND_TIMEDWAIT 0
#define HAVE_PTHREAD_KEY_CREATE 0
#define HAVE_PTHREAD_KEY_DELETE 0
#define HAVE_PTHREAD_SETSPECIFIC 0
#define HAVE_PTHREAD_GETSPECIFIC 0
#define HAVE_PTHREAD_ATFORK 0

/* Locale */
#define HAVE_LOCALE_H 0
#define HAVELANGINFO_H 0
#define HAVE_SETLOCALE 0
#define HAVE_WCSCOLL 0
#define HAVE_WCSXFRM 0

/* Math */
#define HAVE_HYPOT 1
#define HAVE_ATAN2 1
#define HAVE_ACOS 1
#define HAVE_ASIN 1
#define HAVE_EXP 1
#define HAVE_LOG 1
#define HAVE_LOG10 1
#define HAVE_SQRT 1
#define HAVE_FLOOR 1
#define HAVE_CEIL 1
#define HAVE_COPYSIGN 1
#define HAVE_NEXTAFTER 1
#define HAVE_POW 1
#define HAVE_ROUND 1
#define HAVE_FMOD 1
#define HAVE_FREXP 1
#define HAVE_LDEXP 1
#define HAVE_MODF 1
#define HAVE_ISINF 1
#define HAVE_ISNAN 1
#define HAVE_FINITE 1
#define HAVE_TGAMMA 1
#define HAVE_LGAMMA 1
#define HAVE_ERF 1
#define HAVE_ERFC 1
#define HAVE_ACOSH 1
#define HAVE_ASINH 1
#define HAVE_ATANH 1
#define HAVE_SINH 1
#define HAVE_COSH 1
#define HAVE_TANH 1
#define HAVE_ISGREATER 1
#define HAVE_ISGREATEREQUAL 1
#define HAVE_ISLESS 1
#define HAVE_ISLESSEQUAL 1
#define HAVE_ISLESSGREATER 1
#define HAVE_ISUNORDERED 1

/* Python internal features */
#define DOUBLE_IS_LITTLE_ENDIAN_IEEE754 1
#define DOUBLE_IS_BIG_ENDIAN_IEEE754 0
#define DOUBLE_IS_MIXED_ENDIAN_IEEE754 0

/* Disable JIT for now */
#define ENABLE_JIT 0

/* Disable free-threading for now */
#define Py_GIL_DISABLED 0

/* ABI flags */
#define ABIFLAGS ""

/* Version info */
#define VERSION "3.16.0"
#define PY_VERSION "3.16.0"
#define PY_MAJOR_VERSION 3
#define PY_MINOR_VERSION 16
#define PY_MICRO_VERSION 0
#define PY_RELEASE_LEVEL 'a'
#define PY_RELEASE_SERIAL 0

/* Platform string */
#define PLAT "custompython-x86_64"

#endif /* Py_PYCONFIG_H */
