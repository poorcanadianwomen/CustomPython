/* Virtual File System for CustomPython OS
 * Provides file descriptor abstraction and mount points
 */

#include <stdint.h>
#include <stddef.h>

/* File descriptor table */
#define MAX_FD 256

typedef struct {
    int      in_use;
    int      flags;
    uint64_t inode;
    uint64_t offset;
    int      mount_id;
} fd_entry_t;

static fd_entry_t fd_table[MAX_FD];
static int next_fd = 0;

/* Mount point structure */
typedef struct {
    int      in_use;
    char     path[64];
    int      fs_type;
    uint32_t device;
} mount_entry_t;

#define MAX_MOUNTS 16
static mount_entry_t mount_table[MAX_MOUNTS];

/* Initialize VFS */
void vfs_init(void) {
    for (int i = 0; i < MAX_FD; i++) {
        fd_table[i].in_use = 0;
    }
    for (int i = 0; i < MAX_MOUNTS; i++) {
        mount_table[i].in_use = 0;
    }
}

/* Open a file (syscall wrapper) */
int vfs_open(const char *path, int flags, int mode) {
    (void)mode;

    /* Find next free FD */
    int fd = next_fd;
    for (int i = 0; i < MAX_FD; i++) {
        if (!fd_table[i].in_use) {
            fd = i;
            break;
        }
    }

    if (fd >= MAX_FD) return -1;

    /* TODO: Look up file in filesystem */
    /* For now, mark FD as in use */
    fd_table[fd].in_use = 1;
    fd_table[fd].flags = flags;
    fd_table[fd].offset = 0;
    fd_table[fd].mount_id = 0;

    /* Increment next_fd */
    next_fd = (fd + 1) % MAX_FD;

    return fd;
}

/* Close a file */
int vfs_close(int fd) {
    if (fd < 0 || fd >= MAX_FD || !fd_table[fd].in_use) {
        return -1;
    }

    fd_table[fd].in_use = 0;
    return 0;
}

/* Read from a file */
int vfs_read(int fd, void *buf, size_t count) {
    if (fd < 0 || fd >= MAX_FD || !fd_table[fd].in_use) {
        return -1;
    }

    /* TODO: Read from actual filesystem */
    /* For now, return 0 (EOF) */
    (void)buf;
    (void)count;
    return 0;
}

/* Write to a file */
int vfs_write(int fd, const void *buf, size_t count) {
    if (fd < 0 || fd >= MAX_FD || !fd_table[fd].in_use) {
        return -1;
    }

    /* TODO: Write to actual filesystem */
    /* For now, return count (all written) */
    (void)buf;
    (void)count;
    return count;
}

/* Get file status */
int vfs_fstat(int fd, void *stat_buf) {
    if (fd < 0 || fd >= MAX_FD || !fd_table[fd].in_use) {
        return -1;
    }

    /* TODO: Fill in stat structure */
    (void)stat_buf;
    return 0;
}

/* Duplicate a file descriptor */
int vfs_dup(int fd) {
    if (fd < 0 || fd >= MAX_FD || !fd_table[fd].in_use) {
        return -1;
    }

    int new_fd = next_fd;
    for (int i = 0; i < MAX_FD; i++) {
        if (!fd_table[i].in_use) {
            new_fd = i;
            break;
        }
    }

    if (new_fd >= MAX_FD) return -1;

    fd_table[new_fd] = fd_table[fd];
    next_fd = (new_fd + 1) % MAX_FD;

    return new_fd;
}

/* Duplicate fd to specific number */
int vfs_dup2(int oldfd, int newfd) {
    if (oldfd < 0 || oldfd >= MAX_FD || !fd_table[oldfd].in_use) {
        return -1;
    }

    if (newfd < 0 || newfd >= MAX_FD) {
        return -1;
    }

    /* Close newfd if it's open */
    if (fd_table[newfd].in_use) {
        vfs_close(newfd);
    }

    fd_table[newfd] = fd_table[oldfd];
    return newfd;
}

/* Check if fd is a terminal */
int vfs_isatty(int fd) {
    if (fd < 0 || fd >= MAX_FD || !fd_table[fd].in_use) {
        return 0;
    }

    /* fd 0, 1, 2 are considered ttys */
    return (fd <= 2) ? 1 : 0;
}

/* Mount a filesystem */
int vfs_mount(const char *path, int fs_type, uint32_t device) {
    for (int i = 0; i < MAX_MOUNTS; i++) {
        if (!mount_table[i].in_use) {
            mount_table[i].in_use = 1;
            /* Copy path */
            const char *src = path;
            char *dst = mount_table[i].path;
            while (*src && (dst - mount_table[i].path) < 63) {
                *dst++ = *src++;
            }
            *dst = '\0';
            mount_table[i].fs_type = fs_type;
            mount_table[i].device = device;
            return 0;
        }
    }
    return -1;
}
