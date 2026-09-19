/* Heap Allocator for CustomPython OS
 * Simple bump allocator with free list for CPython's malloc/free
 */

#include <stdint.h>
#include <stddef.h>

/* Heap configuration */
#define HEAP_START     0x0000000000400000  /* After kernel */
#define HEAP_SIZE      0x0000000001000000  /* 16MB heap */
#define HEAP_END       (HEAP_START + HEAP_SIZE)

/* Block header (8 bytes) */
typedef struct block_header {
    uint32_t size;          /* Block size (including header) */
    uint8_t  free;          /* 1 = free, 0 = allocated */
    uint8_t  padding[3];    /* Alignment padding */
} block_header_t;

/* Heap state */
static uint8_t *heap_ptr = (uint8_t *)HEAP_START;
static block_header_t *free_list = NULL;

/* Initialize the heap */
void heap_init(void) {
    /* Clear the heap area */
    uint8_t *ptr = (uint8_t *)HEAP_START;
    for (uint64_t i = 0; i < HEAP_SIZE; i++) {
        ptr[i] = 0;
    }

    /* Create initial free block covering entire heap */
    block_header_t *first = (block_header_t *)HEAP_START;
    first->size = HEAP_SIZE;
    first->free = 1;
    free_list = first;

    heap_ptr = (uint8_t *)HEAP_START + sizeof(block_header_t);
}

/* Split a block if it's too large */
static void split_block(block_header_t *block, size_t size) {
    if (block->size >= size + sizeof(block_header_t) + 16) {
        block_header_t *new_block = (block_header_t *)((uint8_t *)block + size);
        new_block->size = block->size - size;
        new_block->free = 1;
        new_block->padding[0] = 0;
        new_block->padding[1] = 0;
        new_block->padding[2] = 0;
        block->size = size;
    }
}

/* Find a free block (first-fit) */
static block_header_t *find_free_block(size_t size) {
    block_header_t *current = free_list;

    while (current != NULL) {
        if (current->free && current->size >= size) {
            return current;
        }
        current = (block_header_t *)((uint8_t *)current + current->size);
    }

    return NULL;
}

/* Merge adjacent free blocks */
static void merge_free_blocks(void) {
    block_header_t *current = (block_header_t *)HEAP_START;

    while ((uint8_t *)current < heap_ptr) {
        if (current->free) {
            block_header_t *next = (block_header_t *)((uint8_t *)current + current->size);
            while ((uint8_t *)next < heap_ptr && next->free) {
                current->size += next->size;
                next = (block_header_t *)((uint8_t *)current + current->size);
            }
        } else {
            current = (block_header_t *)((uint8_t *)current + current->size);
        }
    }
}

/* Allocate memory (called by CPython's malloc) */
void *malloc(size_t size) {
    if (size == 0) return NULL;

    /* Align size to 8 bytes */
    size = (size + 7) & ~7;

    /* Add header size */
    size += sizeof(block_header_t);

    /* Find a free block */
    block_header_t *block = find_free_block(size);

    if (block == NULL) {
        /* No free block found, expand heap */
        if (heap_ptr + size > (uint8_t *)HEAP_END) {
            return NULL;  /* Out of memory */
        }

        block = (block_header_t *)heap_ptr;
        block->size = size;
        block->free = 0;
        heap_ptr += size;
    } else {
        /* Use existing block */
        split_block(block, size);
        block->free = 0;
    }

    /* Return pointer to data (after header) */
    return (void *)((uint8_t *)block + sizeof(block_header_t));
}

/* Free memory (called by CPython's free) */
void free(void *ptr) {
    if (ptr == NULL) return;

    /* Get block header */
    block_header_t *block = (block_header_t *)((uint8_t *)ptr - sizeof(block_header_t));

    /* Validate block */
    if ((uint8_t *)block < (uint8_t *)HEAP_START ||
        (uint8_t *)block >= heap_ptr) {
        return;  /* Invalid pointer */
    }

    /* Mark as free */
    block->free = 1;

    /* Merge adjacent free blocks */
    merge_free_blocks();
}

/* Reallocate memory (called by CPython's realloc) */
void *realloc(void *ptr, size_t size) {
    if (ptr == NULL) return malloc(size);
    if (size == 0) {
        free(ptr);
        return NULL;
    }

    block_header_t *block = (block_header_t *)((uint8_t *)ptr - sizeof(block_header_t));
    size_t old_size = block->size - sizeof(block_header_t);

    if (size <= old_size) {
        return ptr;  /* Current block is large enough */
    }

    /* Allocate new block and copy data */
    void *new_ptr = malloc(size);
    if (new_ptr == NULL) return NULL;

    /* Copy old data */
    uint8_t *src = (uint8_t *)ptr;
    uint8_t *dst = (uint8_t *)new_ptr;
    size_t copy_size = (size < old_size) ? size : old_size;
    for (size_t i = 0; i < copy_size; i++) {
        dst[i] = src[i];
    }

    free(ptr);
    return new_ptr;
}

/* Calloc (called by CPython) */
void *calloc(size_t nmemb, size_t size) {
    size_t total = nmemb * size;
    void *ptr = malloc(total);
    if (ptr != NULL) {
        uint8_t *p = (uint8_t *)ptr;
        for (size_t i = 0; i < total; i++) {
            p[i] = 0;
        }
    }
    return ptr;
}
