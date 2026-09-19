/* cpythonosmodule.c
 * CustomPython OS specific module for CPython
 * Provides OS interface via syscalls
 */

#include "Python.h"
#include "structmember.h"

/* Syscall numbers (must match kernel) */
#define SYS_EXIT           0
#define SYS_READ           1
#define SYS_WRITE          2
#define SYS_OPEN           3
#define SYS_CLOSE          4
#define SYS_FSTAT          5
#define SYS_MMAP           6
#define SYS_MUNMAP         7
#define SYS_BRK            8
#define SYS_NANOSLEEP      9
#define SYS_CLOCK_GETTIME  10
#define SYS_GETCWD         11
#define SYS_CHDIR          12
#define SYS_STAT           13
#define SYS_DUP            14
#define SYS_DUP2           15
#define SYS_PIPE           16
#define SYS_IOCTL          17
#define SYS_GETENV         18
#define SYS_SETENV         19
#define SYS_SIGNAL         20
#define SYS_KILL           21
#define SYS_FORK           22
#define SYS_EXECVE         23
#define SYS_WAITPID        24
#define SYS_GETENTROPY     25
#define SYS_ISATTY         26

/* Clock IDs for clock_gettime */
#define CLOCK_REALTIME              0
#define CLOCK_MONOTONIC             1
#define CLOCK_PROCESS_CPUTIME_ID    2
#define CLOCK_THREAD_CPUTIME_ID     3

/* Time structures */
struct timespec {
    long tv_sec;
    long tv_nsec;
};

/* Inline syscall wrapper */
static inline long syscall1(long num, long arg1) {
    long ret;
    __asm__ volatile (
        "syscall"
        : "=a"(ret)
        : "a"(num), "D"(arg1)
        : "rcx", "r11", "memory"
    );
    return ret;
}

static inline long syscall2(long num, long arg1, long arg2) {
    long ret;
    __asm__ volatile (
        "syscall"
        : "=a"(ret)
        : "a"(num), "D"(arg1), "S"(arg2)
        : "rcx", "r11", "memory"
    );
    return ret;
}

static inline long syscall3(long num, long arg1, long arg2, long arg3) {
    long ret;
    __asm__ volatile (
        "syscall"
        : "=a"(ret)
        : "a"(num), "D"(arg1), "S"(arg2), "d"(arg3)
        : "rcx", "r11", "memory"
    );
    return ret;
}

static inline long syscall6(long num, long arg1, long arg2, long arg3,
                            long arg4, long arg5, long arg6) {
    long ret;
    register long r10 __asm__("r10") = arg4;
    register long r8 __asm__("r8") = arg5;
    register long r9 __asm__("r9") = arg6;
    __asm__ volatile (
        "syscall"
        : "=a"(ret)
        : "a"(num), "D"(arg1), "S"(arg2), "d"(arg3),
          "r"(r10), "r"(r8), "r"(r9)
        : "rcx", "r11", "memory"
    );
    return ret;
}

/* os.read(fd, count) -> bytes */
static PyObject *
cpythonos_read(PyObject *self, PyObject *args)
{
    int fd;
    Py_ssize_t count;

    if (!PyArg_ParseTuple(args, "in", &fd, &count))
        return NULL;

    if (count < 0) {
        PyErr_SetString(PyExc_ValueError, "count must be non-negative");
        return NULL;
    }

    if (count == 0) {
        return PyBytes_FromStringAndSize("", 0);
    }

    char *buf = PyMem_Malloc(count);
    if (buf == NULL) {
        return PyErr_NoMemory();
    }

    ssize_t result = syscall3(SYS_READ, fd, (long)buf, count);

    if (result < 0) {
        PyMem_Free(buf);
        PyErr_SetFromErrno(PyExc_OSError);
        return NULL;
    }

    PyObject *bytes_obj = PyBytes_FromStringAndSize(buf, result);
    PyMem_Free(buf);
    return bytes_obj;
}

/* os.write(fd, data) -> int */
static PyObject *
cpythonos_write(PyObject *self, PyObject *args)
{
    int fd;
    Py_buffer data;

    if (!PyArg_ParseTuple(args, "iy*", &fd, &data))
        return NULL;

    ssize_t result = syscall3(SYS_WRITE, fd, (long)data.buf, data.len);

    PyBuffer_Release(&data);

    if (result < 0) {
        PyErr_SetFromErrno(PyExc_OSError);
        return NULL;
    }

    return PyLong_FromSsize_t(result);
}

/* os.open(path, flags, mode) -> int */
static PyObject *
cpythonos_open(PyObject *self, PyObject *args)
{
    const char *path;
    int flags;
    int mode = 0;

    if (!PyArg_ParseTuple(args, "si|i", &path, &flags, &mode))
        return NULL;

    long result = syscall3(SYS_OPEN, (long)path, flags, mode);

    if (result < 0) {
        PyErr_SetFromErrno(PyExc_OSError);
        return NULL;
    }

    return PyLong_FromLong(result);
}

/* os.close(fd) -> None */
static PyObject *
cpythonos_close(PyObject *self, PyObject *args)
{
    int fd;

    if (!PyArg_ParseTuple(args, "i", &fd))
        return NULL;

    long result = syscall1(SYS_CLOSE, fd);

    if (result < 0) {
        PyErr_SetFromErrno(PyExc_OSError);
        return NULL;
    }

    Py_RETURN_NONE;
}

/* os.fstat(fd) -> stat_result */
static PyObject *
cpythonos_fstat(PyObject *self, PyObject *args)
{
    int fd;

    if (!PyArg_ParseTuple(args, "i", &fd))
        return NULL;

    /* TODO: Implement fstat syscall */
    PyErr_SetString(PyExc_NotImplementedError, "fstat not implemented");
    return NULL;
}

/* os.getcwd() -> str */
static PyObject *
cpythonos_getcwd(PyObject *self, PyObject *Py_UNUSED(ignored))
{
    char buf[4096];

    long result = syscall2(SYS_GETCWD, (long)buf, sizeof(buf));

    if (result < 0) {
        PyErr_SetFromErrno(PyExc_OSError);
        return NULL;
    }

    return PyUnicode_FromString(buf);
}

/* os.chdir(path) -> None */
static PyObject *
cpythonos_chdir(PyObject *self, PyObject *args)
{
    const char *path;

    if (!PyArg_ParseTuple(args, "s", &path))
        return NULL;

    long result = syscall1(SYS_CHDIR, (long)path);

    if (result < 0) {
        PyErr_SetFromErrno(PyExc_OSError);
        return NULL;
    }

    Py_RETURN_NONE;
}

/* os.fork() -> int */
static PyObject *
cpythonos_fork(PyObject *self, PyObject *Py_UNUSED(ignored))
{
    long result = syscall1(SYS_FORK, 0);

    if (result < 0) {
        PyErr_SetFromErrno(PyExc_OSError);
        return NULL;
    }

    return PyLong_FromLong(result);
}

/* os.execve(path, argv, envp) -> None */
static PyObject *
cpythonos_execve(PyObject *self, PyObject *args)
{
    const char *path;
    PyObject *argv_list;
    PyObject *envp_list;

    if (!PyArg_ParseTuple(args, "sOO", &path, &argv_list, &envp_list))
        return NULL;

    /* TODO: Convert Python lists to C arrays and call execve */
    PyErr_SetString(PyExc_NotImplementedError, "execve not implemented");
    return NULL;
}

/* os.waitpid(pid, options) -> (pid, status) */
static PyObject *
cpythonos_waitpid(PyObject *self, PyObject *args)
{
    int pid;
    int options;

    if (!PyArg_ParseTuple(args, "ii", &pid, &options))
        return NULL;

    /* TODO: Implement waitpid */
    PyErr_SetString(PyExc_NotImplementedError, "waitpid not implemented");
    return NULL;
}

/* os.getpid() -> int */
static PyObject *
cpythonos_getpid(PyObject *self, PyObject *Py_UNUSED(ignored))
{
    /* TODO: Implement getpid syscall */
    return PyLong_FromLong(1);
}

/* os.getuid() -> int */
static PyObject *
cpythonos_getuid(PyObject *self, PyObject *Py_UNUSED(ignored))
{
    return PyLong_FromLong(0);
}

/* os.geteuid() -> int */
static PyObject *
cpythonos_geteuid(PyObject *self, PyObject *Py_UNUSED(ignored))
{
    return PyLong_FromLong(0);
}

/* os.getgid() -> int */
static PyObject *
cpythonos_getgid(PyObject *self, PyObject *Py_UNUSED(ignored))
{
    return PyLong_FromLong(0);
}

/* os.getegid() -> int */
static PyObject *
cpythonos_getegid(PyObject *self, PyObject *Py_UNUSED(ignored))
{
    return PyLong_FromLong(0);
}

/* os.isatty(fd) -> bool */
static PyObject *
cpythonos_isatty(PyObject *self, PyObject *args)
{
    int fd;

    if (!PyArg_ParseTuple(args, "i", &fd))
        return NULL;

    long result = syscall1(SYS_ISATTY, fd);

    return PyBool_FromLong(result);
}

/* os.strerror(code) -> str */
static PyObject *
cpythonos_strerror(PyObject *self, PyObject *args)
{
    int code;

    if (!PyArg_ParseTuple(args, "i", &code))
        return NULL;

    /* Simple strerror implementation */
    const char *msg = "Unknown error";
    switch (code) {
        case 0: msg = "Success"; break;
        case 1: msg = "Operation not permitted"; break;
        case 2: msg = "No such file or directory"; break;
        case 3: msg = "No such process"; break;
        case 4: msg = "Interrupted system call"; break;
        case 5: msg = "I/O error"; break;
        case 6: msg = "No such device or address"; break;
        case 7: msg = "Argument list too long"; break;
        case 8: msg = "Exec format error"; break;
        case 9: msg = "Bad file descriptor"; break;
        case 10: msg = "No child processes"; break;
        case 11: msg = "Resource temporarily unavailable"; break;
        case 12: msg = "Out of memory"; break;
        case 13: msg = "Permission denied"; break;
        case 14: msg = "Bad address"; break;
        case 16: msg = "Device or resource busy"; break;
        case 17: msg = "File exists"; break;
        case 18: msg = "Invalid argument"; break;
        case 19: msg = "No such device"; break;
        case 20: msg = "Not a directory"; break;
        case 21: msg = "Is a directory"; break;
        case 22: msg = "Invalid argument"; break;
        case 23: msg = "Too many open files in system"; break;
        case 24: msg = "Too many open files"; break;
        case 25: msg = "Not a typewriter"; break;
        case 26: msg = "Text file busy"; break;
        case 27: msg = "File too large"; break;
        case 28: msg = "No space left on device"; break;
        case 29: msg = "Illegal seek"; break;
        case 30: msg = "Read-only file system"; break;
        case 31: msg = "Too many links"; break;
        case 32: msg = "Broken pipe"; break;
        case 33: msg = "Numerical argument out of domain"; break;
        case 34: msg = "Numerical result out of range"; break;
        case 35: msg = "Resource deadlock avoided"; break;
        case 36: msg = "File name too long"; break;
        case 37: msg = "No locks available"; break;
        case 38: msg = "Function not implemented"; break;
        case 39: msg = "Directory not empty"; break;
        case 40: msg = "Too many levels of symbolic links"; break;
    }

    return PyUnicode_FromString(msg);
}

/* os.getenv(name, default=None) -> str or None */
static PyObject *
cpythonos_getenv(PyObject *self, PyObject *args)
{
    const char *name;
    PyObject *default_value = Py_None;

    if (!PyArg_ParseTuple(args, "s|O", &name, &default_value))
        return NULL;

    /* TODO: Implement getenv syscall */
    Py_INCREF(default_value);
    return default_value;
}

/* os.environ -> dict */
static PyObject *
cpythonos_environ(PyObject *self, PyObject *Py_UNUSED(ignored))
{
    /* TODO: Return actual environment variables */
    return PyDict_New();
}

/* os.urandom(n) -> bytes */
static PyObject *
cpythonos_urandom(PyObject *self, PyObject *args)
{
    int n;

    if (!PyArg_ParseTuple(args, "i", &n))
        return NULL;

    if (n < 0) {
        PyErr_SetString(PyExc_ValueError, "n must be non-negative");
        return NULL;
    }

    char *buf = PyMem_Malloc(n);
    if (buf == NULL) {
        return PyErr_NoMemory();
    }

    long result = syscall2(SYS_GETENTROPY, (long)buf, n);

    if (result < 0) {
        PyMem_Free(buf);
        PyErr_SetFromErrno(PyExc_OSError);
        return NULL;
    }

    PyObject *bytes_obj = PyBytes_FromStringAndSize(buf, n);
    PyMem_Free(buf);
    return bytes_obj;
}

/* os.kill(pid, sig) -> None */
static PyObject *
cpythonos_kill(PyObject *self, PyObject *args)
{
    int pid;
    int sig;

    if (!PyArg_ParseTuple(args, "ii", &pid, &sig))
        return NULL;

    long result = syscall2(SYS_KILL, pid, sig);

    if (result < 0) {
        PyErr_SetFromErrno(PyExc_OSError);
        return NULL;
    }

    Py_RETURN_NONE;
}

/* os.pipe() -> (read_fd, write_fd) */
static PyObject *
cpythonos_pipe(PyObject *self, PyObject *Py_UNUSED(ignored))
{
    int pipefd[2];

    long result = syscall1(SYS_PIPE, (long)pipefd);

    if (result < 0) {
        PyErr_SetFromErrno(PyExc_OSError);
        return NULL;
    }

    return Py_BuildValue("(ii)", pipefd[0], pipefd[1]);
}

/* os.dup(fd) -> int */
static PyObject *
cpythonos_dup(PyObject *self, PyObject *args)
{
    int fd;

    if (!PyArg_ParseTuple(args, "i", &fd))
        return NULL;

    long result = syscall1(SYS_DUP, fd);

    if (result < 0) {
        PyErr_SetFromErrno(PyExc_OSError);
        return NULL;
    }

    return PyLong_FromLong(result);
}

/* os.dup2(old_fd, new_fd) -> int */
static PyObject *
cpythonos_dup2(PyObject *self, PyObject *args)
{
    int old_fd;
    int new_fd;

    if (!PyArg_ParseTuple(args, "ii", &old_fd, &new_fd))
        return NULL;

    long result = syscall2(SYS_DUP2, old_fd, new_fd);

    if (result < 0) {
        PyErr_SetFromErrno(PyExc_OSError);
        return NULL;
    }

    return PyLong_FromLong(result);
}

/* Method table */
static PyMethodDef cpythonos_methods[] = {
    {"read", cpythonos_read, METH_VARARGS, "Read from a file descriptor"},
    {"write", cpythonos_write, METH_VARARGS, "Write to a file descriptor"},
    {"open", cpythonos_open, METH_VARARGS, "Open a file"},
    {"close", cpythonos_close, METH_VARARGS, "Close a file descriptor"},
    {"fstat", cpythonos_fstat, METH_VARARGS, "Get file status"},
    {"getcwd", cpythonos_getcwd, METH_NOARGS, "Get current working directory"},
    {"chdir", cpythonos_chdir, METH_VARARGS, "Change working directory"},
    {"fork", cpythonos_fork, METH_NOARGS, "Fork process"},
    {"execve", cpythonos_execve, METH_VARARGS, "Execute program"},
    {"waitpid", cpythonos_waitpid, METH_VARARGS, "Wait for process"},
    {"getpid", cpythonos_getpid, METH_NOARGS, "Get process ID"},
    {"getuid", cpythonos_getuid, METH_NOARGS, "Get user ID"},
    {"geteuid", cpythonos_geteuid, METH_NOARGS, "Get effective user ID"},
    {"getgid", cpythonos_getgid, METH_NOARGS, "Get group ID"},
    {"getegid", cpythonos_getegid, METH_NOARGS, "Get effective group ID"},
    {"isatty", cpythonos_isatty, METH_VARARGS, "Test if fd is a terminal"},
    {"strerror", cpythonos_strerror, METH_VARARGS, "Get error string"},
    {"getenv", cpythonos_getenv, METH_VARARGS, "Get environment variable"},
    {"urandom", cpythonos_urandom, METH_VARARGS, "Get random bytes"},
    {"kill", cpythonos_kill, METH_VARARGS, "Send signal to process"},
    {"pipe", cpythonos_pipe, METH_NOARGS, "Create pipe"},
    {"dup", cpythonos_dup, METH_VARARGS, "Duplicate file descriptor"},
    {"dup2", cpythonos_dup2, METH_VARARGS, "Duplicate file descriptor to specific number"},
    {NULL, NULL, 0, NULL}
};

/* Module definition */
static struct PyModuleDef cpythonosmodule = {
    PyModuleDef_HEAD_INIT,
    "_cpythonos",
    "CustomPython OS interface module",
    -1,
    cpythonos_methods
};

/* Module initialization */
PyMODINIT_FUNC
PyInit__cpythonos(void)
{
    PyObject *m;

    m = PyModule_Create(&cpythonosmodule);
    if (m == NULL)
        return NULL;

    /* Add constants */
    PyModule_AddIntConstant(m, "O_RDONLY", 0);
    PyModule_AddIntConstant(m, "O_WRONLY", 1);
    PyModule_AddIntConstant(m, "O_RDWR", 2);
    PyModule_AddIntConstant(m, "O_CREAT", 64);
    PyModule_AddIntConstant(m, "O_EXCL", 128);
    PyModule_AddIntConstant(m, "O_TRUNC", 512);
    PyModule_AddIntConstant(m, "O_APPEND", 1024);
    PyModule_AddIntConstant(m, "O_NONBLOCK", 2048);

    PyModule_AddIntConstant(m, "S_ISUID", 04000);
    PyModule_AddIntConstant(m, "S_ISGID", 02000);
    PyModule_AddIntConstant(m, "S_IRUSR", 0400);
    PyModule_AddIntConstant(m, "S_IWUSR", 0200);
    PyModule_AddIntConstant(m, "S_IXUSR", 0100);
    PyModule_AddIntConstant(m, "S_IRGRP", 040);
    PyModule_AddIntConstant(m, "S_IWGRP", 020);
    PyModule_AddIntConstant(m, "S_IXGRP", 010);
    PyModule_AddIntConstant(m, "S_IROTH", 04);
    PyModule_AddIntConstant(m, "S_IWOTH", 02);
    PyModule_AddIntConstant(m, "S_IXOTH", 01);

    PyModule_AddIntConstant(m, "CLOCK_REALTIME", 0);
    PyModule_AddIntConstant(m, "CLOCK_MONOTONIC", 1);

    PyModule_AddStringConstant(m, "name", "custompython");

    /* Add environ dict */
    PyObject *environ = cpythonos_environ(NULL, NULL);
    if (environ != NULL) {
        PyModule_AddObject(m, "environ", environ);
    }

    return m;
}
